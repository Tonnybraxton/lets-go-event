from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_location_suggestion"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not started"),
                    ("PENDING", "Pending"),
                    ("COMPLETED", "Completed"),
                    ("FAILED", "Failed"),
                ],
                default="NOT_STARTED",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="checkout_request_id",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="order",
            name="merchant_request_id",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="order",
            name="mpesa_receipt_number",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_result_desc",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

