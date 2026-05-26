from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
)

from modules.scan.upload import validate_upload
from modules.scan.ocr import extract_text

from modules.scan.product_lookup import lookup_product
from modules.scan.product_image import get_product_image

from modules.scan.confidence import calculate_confidence
from modules.scan.health_badge import generate_badge

from modules.scan.scan_history import (
    save_scan,
    get_history,
)

from modules.scan.favorites import (
    add_favorite,
    get_favorites,
)

from modules.scan.manual import (
    parse_manual_input,
)

from modules.scan.positives import (
    get_positives,
)

from modules.scan.negatives import (
    get_negatives,
)

from modules.scan.risk_alert import (
    detect_risks,
)

from modules.scan.allergens import (
    detect_allergens,
)

from modules.scan.barcode import (
    extract_barcode,
)

from modules.scan.product_lookup_api import (
    lookup_external,
)

from modules.scan.nutriscore import (
    compute_nutriscore,
)

from modules.scan.nova import (
    compute_nova,
)

from modules.scan.barcode_ai import (
    analyze_barcode,
)


router = APIRouter()


async def process_scan(
    file: UploadFile,
):

    upload = await validate_upload(
        file
    )

    ocr = await extract_text(
        file
    )

    product = lookup_product(
        ocr["text"]
    )

    image = get_product_image(
        product
    )

    confidence = calculate_confidence(
        ocr,
        product,
    )

    badge = generate_badge(
        product
    )

    positives = get_positives(
        ocr["text"]
    )

    negatives = get_negatives(
        ocr["text"]
    )

    risks = detect_risks(
        ocr["text"]
    )

    allergens = detect_allergens(
        ocr["text"]
    )

    barcode = extract_barcode(
        ocr["text"]
    )

    nutrition = await lookup_external(
        barcode
    )

    nutriscore = compute_nutriscore(
        negatives
    )

    nova = compute_nova(
        negatives
    )

    result = {

        "product": {

            **product,

            "image": image,

        },

        "upload": upload,

        "confidence": confidence,

        "health_badge": badge,

        "positives": positives,

        "negatives": negatives,

        "risk_alerts": risks,

        "allergens": allergens,

        "barcode": barcode,

        "nutrition_autofill": nutrition,

        "nutriscore": nutriscore,

        "nova": nova,

    }

    save_scan(
        result
    )

    add_favorite(
        result[
            "product"
        ]
    )

    return result


@router.post("/")
async def scan(

    file: UploadFile = File(
        ...
    ),

):

    result = await process_scan(
        file
    )

    return {

        "success": True,

        **result,

    }


@router.post(
    "/manual"
)
async def manual(

    product: str = Form(
        ...
    ),

):

    return {

        "success": True,

        "manual":
        parse_manual_input(
            product
        ),

    }


@router.post(
    "/multi"
)
async def multi(

    files: list[UploadFile],

):

    results = []

    for file in files:

        results.append(

            await process_scan(
                file
            )

        )

    return {

        "success": True,

        "total": len(
            results
        ),

        "results": results,

    }


@router.post(
    "/barcode/analyze"
)
async def barcode_analysis(

    barcode: str = Form(
        ...
    ),

):

    product = {

        "brand":
        "Unknown",

        "category":
        "food",

    }

    analysis = await analyze_barcode(

        barcode,

        product,

    )

    return {

        "success": True,

        "analysis":
        analysis,

    }


@router.get(
    "/history"
)
async def history():

    return {

        "history":
        get_history()

    }


@router.get(
    "/favorites"
)
async def favorites():

    return {

        "favorites":
        get_favorites()

    }