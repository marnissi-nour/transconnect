from decimal import Decimal


VEHICLE_WEIGHT_LIMITS = {
    "camionnette": (Decimal("0"), Decimal("1500")),
    "fourgon": (Decimal("0"), Decimal("3500")),
    "camion_porteur": (Decimal("3500"), Decimal("19000")),
    "semi_remorque": (Decimal("19000"), Decimal("26000")),
}
