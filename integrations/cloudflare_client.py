"""
🔴💀 Cloudflare Client — R2, KV, D1, Workers integration
"""
import os
import json
from typing import Any, Dict, Optional
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CF_R2_API = os.getenv("CLOUDFLARE_R2_S3_API", "")
CF_WORKER_TOKEN = os.getenv("CLOUDFLARE_WORKER_TOKEN", "")

R2_BUCKET = "red-team-reports"
KV_NAMESPACE = "red-team-sessions"


class CloudflareClient:
    """Client for Cloudflare R2, KV, D1, and Workers."""

    def __init__(self):
        self._base = f"https://api.cloudflare.com/client/v4"
        self._headers = {
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self._client = httpx.Client(headers=self._headers, timeout=30)

    # ── R2 Object Storage ─────────────────────────────────────────────────────

    def upload_report(self, session_id: str, content: str, bucket: str = R2_BUCKET) -> bool:
        """Upload a report to R2."""
        try:
            import boto3
            access_key = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", CF_ACCOUNT_ID)
            secret_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", CF_API_TOKEN)
            s3 = boto3.client(
                "s3",
                endpoint_url=CF_R2_API,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="auto",
            )
            key = f"reports/{session_id}/report.md"
            s3.put_object(Bucket=bucket, Key=key, Body=content.encode(), ContentType="text/markdown")
            logger.info(f"[Cloudflare/R2] Uploaded report: {key}")
            return True
        except Exception as e:
            logger.error(f"[Cloudflare/R2] Upload failed: {e}")
            return False

    def download_report(self, session_id: str, bucket: str = R2_BUCKET) -> Optional[str]:
        """Download a report from R2."""
        try:
            import boto3
            access_key = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", CF_ACCOUNT_ID)
            secret_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", CF_API_TOKEN)
            s3 = boto3.client(
                "s3",
                endpoint_url=CF_R2_API,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="auto",
            )
            key = f"reports/{session_id}/report.md"
            obj = s3.get_object(Bucket=bucket, Key=key)
            return obj["Body"].read().decode()
        except Exception as e:
            logger.error(f"[Cloudflare/R2] Download failed: {e}")
            return None

    def list_reports(self, bucket: str = R2_BUCKET) -> list:
        """List all reports in R2."""
        try:
            import boto3
            access_key = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", CF_ACCOUNT_ID)
            secret_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", CF_API_TOKEN)
            s3 = boto3.client(
                "s3",
                endpoint_url=CF_R2_API,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="auto",
            )
            resp = s3.list_objects_v2(Bucket=bucket, Prefix="reports/")
            return [obj["Key"] for obj in resp.get("Contents", [])]
        except Exception as e:
            logger.error(f"[Cloudflare/R2] List failed: {e}")
            return []

    # ── KV Store ──────────────────────────────────────────────────────────────

    def kv_put(self, key: str, value: Any, namespace_id: str = "") -> bool:
        """Write to Cloudflare KV."""
        try:
            ns = namespace_id or os.getenv("CF_KV_NAMESPACE_ID", "")
            url = f"{self._base}/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{ns}/values/{key}"
            body = json.dumps(value) if not isinstance(value, str) else value
            resp = self._client.put(url, content=body.encode())
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"[Cloudflare/KV] Put failed: {e}")
            return False

    def kv_get(self, key: str, namespace_id: str = "") -> Optional[str]:
        """Read from Cloudflare KV."""
        try:
            ns = namespace_id or os.getenv("CF_KV_NAMESPACE_ID", "")
            url = f"{self._base}/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{ns}/values/{key}"
            resp = self._client.get(url)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logger.error(f"[Cloudflare/KV] Get failed: {e}")
            return None

    # ── Workers ──────────────────────────────────────────────────────────────

    def invoke_worker(self, worker_url: str, payload: Dict) -> Dict:
        """Call a Cloudflare Worker endpoint."""
        try:
            resp = httpx.post(
                worker_url,
                json=payload,
                headers={"Authorization": f"Bearer {CF_WORKER_TOKEN}"},
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"[Cloudflare/Worker] Invoke failed: {e}")
            return {"error": str(e)}

    # ── Stream Video ─────────────────────────────────────────────────────────

    def upload_video(self, file_path: str) -> Optional[str]:
        """Upload a video to Cloudflare Stream."""
        try:
            url = f"{self._base}/accounts/{CF_ACCOUNT_ID}/stream"
            with open(file_path, "rb") as f:
                resp = self._client.post(url, content=f.read())
            resp.raise_for_status()
            video_id = resp.json()["result"]["uid"]
            logger.info(f"[Cloudflare/Stream] Uploaded video: {video_id}")
            return video_id
        except Exception as e:
            logger.error(f"[Cloudflare/Stream] Upload failed: {e}")
            return None

    # ── Images ───────────────────────────────────────────────────────────────

    def upload_image(self, file_path: str, metadata: Optional[Dict] = None) -> Optional[str]:
        """Upload an image to Cloudflare Images."""
        try:
            url = f"{self._base}/accounts/{CF_ACCOUNT_ID}/images/v1"
            files = {"file": open(file_path, "rb")}
            data = {"metadata": json.dumps(metadata or {})}
            resp = self._client.post(url, files=files, data=data)
            resp.raise_for_status()
            image_id = resp.json()["result"]["id"]
            logger.info(f"[Cloudflare/Images] Uploaded image: {image_id}")
            return image_id
        except Exception as e:
            logger.error(f"[Cloudflare/Images] Upload failed: {e}")
            return None

    def close(self):
        self._client.close()
