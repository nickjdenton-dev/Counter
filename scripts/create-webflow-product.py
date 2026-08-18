#!/usr/bin/env python3
"""Create the Count Blackjack Unlock digital product on JD's Pharmacopeia.

Webflow's CMS item endpoints reject ecommerce collections (403). This uses
the Ecommerce Products API instead:

  POST /v2/sites/{site_id}/products
  PATCH /v2/collections/{sku_collection_id}/items/{sku_id}/inventory

Requires WEBFLOW_TOKEN with ecommerce:write (site token or OAuth).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

SITE_ID = "60f794aa5c6aabbdaef6fa21"
SKU_COLLECTION_ID = "60f794aa5c6aab5b27f6fa43"
APOTHECARY_CATEGORY_ID = "60f794aa5c6aabb9b4f6fa41"
DIGITAL_PRODUCT_TYPE = "f22027db68002190aef89a4a2b7ac8a1"
PRODUCT_SLUG = "count-blackjack"
API = "https://api.webflow.com/v2"


def request(method: str, path: str, token: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{method} {path} failed ({exc.code}): {detail}") from exc


def list_existing(token: str) -> dict | None:
    offset = 0
    while True:
        payload = request(
            "GET",
            f"/sites/{SITE_ID}/products?limit=100&offset={offset}",
            token,
        )
        items = payload.get("items") or payload.get("products") or []
        for item in items:
            product = item.get("product", item)
            field = product.get("fieldData") or {}
            if field.get("slug") == PRODUCT_SLUG:
                return item
        pagination = payload.get("pagination") or {}
        total = pagination.get("total", len(items))
        offset += len(items)
        if not items or offset >= total:
            return None


def product_payload() -> dict:
    description = (
        "Learn the Hi-Lo card counting system while playing real blackjack. "
        "Lite (Learn mode) is free. Practice mode is included in a 5-day trial, "
        "then unlocks with this $0.99 key from JDs Pharmacopeia.\n\n"
        "After checkout you will receive an unlock key like CB-XXXX-XXXX-XXXX. "
        "Open Count Blackjack, tap Enter unlock key, and paste it. Lite Learn "
        "mode stays free either way."
    )
    how_to_use = (
        "1. Complete checkout for this $0.99 digital unlock (no shipping).\n"
        "2. Copy your key from the order confirmation (format CB-XXXX-XXXX-XXXX).\n"
        "3. Open Count Blackjack on your phone.\n"
        "4. Tap Enter unlock key, paste the key, and tap Unlock with key.\n"
        "5. Practice mode stays unlocked on this device. Lite Learn mode stays free either way."
    )
    additional = (
        "This is a learning tool for the Hi-Lo card counting system. Counting cards "
        "is legal; casinos can still refuse service. Nothing is shipped. Instant "
        "digital delivery — no physical product.\n\n"
        "If you paid Venmo or Cash App @JDsPharmacopeia instead of checkout, "
        "message JD with your payment and we will send a key."
    )
    return {
        "publishStatus": "live",
        "product": {
            "fieldData": {
                "name": "Count Blackjack Unlock",
                "slug": PRODUCT_SLUG,
                "description": description,
                "shippable": False,
                "tax-category": "digital-goods",
                "ec-product-type": DIGITAL_PRODUCT_TYPE,
                "category": [APOTHECARY_CATEGORY_ID],
                "how-to-use": how_to_use,
                "additional-information": additional,
                "featured-product-description": (
                    "A $0.99 unlock key for Count Blackjack Practice mode — "
                    "hidden counts and running-count quizzes."
                ),
            }
        },
        "sku": {
            "fieldData": {
                "name": "Count Blackjack Unlock",
                "slug": PRODUCT_SLUG,
                "sku": "CB-UNLOCK-099",
                "price": {"value": 99, "unit": "USD", "currency": "USD"},
                "ec-sku-billing-method": "one-time",
            }
        },
    }


def set_infinite_inventory(token: str, sku_id: str) -> dict:
    return request(
        "PATCH",
        f"/collections/{SKU_COLLECTION_ID}/items/{sku_id}/inventory",
        token,
        {"inventoryType": "infinite"},
    )


def main() -> None:
    token = os.environ.get("WEBFLOW_TOKEN") or os.environ.get("WEBFLOW_SITE_API_TOKEN")
    if not token:
        raise SystemExit(
            "Set WEBFLOW_TOKEN (ecommerce:write) and rerun:\n"
            "  WEBFLOW_TOKEN=... python3 scripts/create-webflow-product.py"
        )

    existing = list_existing(token)
    if existing:
        product = existing.get("product", existing)
        sku = (existing.get("skus") or [None])[0]
        print("Product already exists:")
        print(json.dumps({"product": product, "sku": sku}, indent=2))
        sku_id = (sku or {}).get("id")
        if sku_id:
            print("Setting infinite inventory…")
            print(json.dumps(set_infinite_inventory(token, sku_id), indent=2))
        print("https://www.jdspharmacopeia.com/product/count-blackjack")
        return

    created = request("POST", f"/sites/{SITE_ID}/products", token, product_payload())
    print(json.dumps(created, indent=2))
    sku = (created.get("skus") or [None])[0]
    sku_id = (sku or {}).get("id")
    if sku_id:
        print("Setting infinite inventory…")
        print(json.dumps(set_infinite_inventory(token, sku_id), indent=2))
    print("Live URL: https://www.jdspharmacopeia.com/product/count-blackjack")


if __name__ == "__main__":
    main()
