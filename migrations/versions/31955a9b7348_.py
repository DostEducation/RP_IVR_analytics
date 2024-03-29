"""empty message

Revision ID: 31955a9b7348
Revises:
Create Date: 2023-10-13 17:57:05.435944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "31955a9b7348"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bigquery_jobs",
        sa.Column("table_name", sa.String(length=100), nullable=False),
        sa.Column("index", sa.String(length=100), server_default="0", nullable=True),
        sa.Column("bigquery_table_name", sa.String(length=100), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column(
            "last_updated_at",
            sa.DateTime(),
            server_default="2000-01-01 00:00:00",
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("table_name"),
    )
    op.create_table(
        "call_log_event",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("call_sid", sa.String(length=255), nullable=True),
        sa.Column("account_sid", sa.String(length=255), nullable=True),
        sa.Column("from_number", sa.String(length=255), nullable=True),
        sa.Column("to_number", sa.String(length=255), nullable=True),
        sa.Column("call_status", sa.String(length=255), nullable=True),
        sa.Column("direction", sa.String(length=255), nullable=True),
        sa.Column("parent_call_sid", sa.String(length=255), nullable=True),
        sa.Column("telco_code", sa.String(length=255), nullable=True),
        sa.Column("telco_status", sa.String(length=255), nullable=True),
        sa.Column("dial_time", sa.DateTime(), nullable=True),
        sa.Column("pick_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("duration", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contact_fields_mapping",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("field_type", sa.String(length=255), nullable=True),
        sa.Column("field_name", sa.String(length=255), nullable=True),
        sa.Column("mapped_table_name", sa.String(length=255), nullable=True),
        sa.Column("mapped_table_column_name", sa.String(length=255), nullable=True),
        sa.Column("mapped_table_column_value", sa.String(length=255), nullable=True),
        sa.Column("expected_field_data_type", sa.String(length=255), nullable=True),
        sa.Column("expected_field_value", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "content",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "ivr_callback_transaction_log",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("processed", sa.Boolean(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "language",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "partner",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "program",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("discontinuation_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("program_type", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "system_phone",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "webhook_transaction_log",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("processed", sa.Boolean(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "content_version",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("language_id", sa.Integer(), nullable=True),
        sa.Column("version", sa.Float(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["content_id"], ["content.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["language_id"], ["language.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ivr_prompt",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prompt_name", sa.String(length=255), nullable=False),
        sa.Column("prompt_question", sa.String(length=500), nullable=True),
        sa.Column("possible_response", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("keypress", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["content.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "module",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "partner_system_phone",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("partner_id", sa.Integer(), nullable=True),
        sa.Column("system_phone_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["partner_id"],
            ["partner.id"],
        ),
        sa.ForeignKeyConstraint(
            ["system_phone_id"],
            ["system_phone.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("address_line_1", sa.String(length=500), nullable=True),
        sa.Column("address_line_2", sa.String(length=500), nullable=True),
        sa.Column("postal_code", sa.String(length=50), nullable=True),
        sa.Column("partner_id", sa.Integer(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["partner_id"],
            ["partner.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "ivr_prompt_mapping",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ivr_prompt_id", sa.Integer(), nullable=True),
        sa.Column("mapped_table_name", sa.String(length=255), nullable=True),
        sa.Column("mapped_table_column_name", sa.String(length=255), nullable=True),
        sa.Column("default_value", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["ivr_prompt_id"],
            ["ivr_prompt.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ivr_prompt_response",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prompt_name", sa.String(length=255), nullable=False),
        sa.Column("prompt_question", sa.String(length=500), nullable=True),
        sa.Column("response", sa.String(length=255), nullable=True),
        sa.Column("user_phone", sa.String(length=50), nullable=True),
        sa.Column("is_call_log_processed", sa.Boolean(), nullable=True),
        sa.Column("call_sid", sa.Integer(), nullable=True),
        sa.Column("call_log_id", sa.Integer(), nullable=True),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("content_version_id", sa.Integer(), nullable=True),
        sa.Column("keypress", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["content.id"],
        ),
        sa.ForeignKeyConstraint(
            ["content_version_id"],
            ["content_version.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "module_content",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=True),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("is_optional", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["content.id"],
        ),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["module.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "program_module",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.Column("module_id", sa.Integer(), nullable=True),
        sa.Column("sequence", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["module.id"],
        ),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "program_sequence",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.Column("module_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["content.id"],
        ),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["module.id"],
        ),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "registration",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("user_phone", sa.String(length=50), nullable=False),
        sa.Column("system_phone", sa.String(length=50), nullable=False),
        sa.Column("partner_id", sa.Integer(), nullable=True),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("education_level", sa.String(length=255), nullable=True),
        sa.Column("occupation", sa.String(length=255), nullable=True),
        sa.Column("gender_of_child", sa.String(length=255), nullable=True),
        sa.Column("number_of_eligible_kids", sa.String(length=255), nullable=True),
        sa.Column("area_type", sa.String(length=255), nullable=True),
        sa.Column("parent_type", sa.String(length=50), nullable=True),
        sa.Column("is_child_between_0_3", sa.Boolean(), nullable=True),
        sa.Column("is_child_between_3_6", sa.Boolean(), nullable=True),
        sa.Column("is_child_above_6", sa.Boolean(), nullable=True),
        sa.Column("has_no_child", sa.Boolean(), nullable=True),
        sa.Column("has_smartphone", sa.Boolean(), nullable=True),
        sa.Column("has_dropped_missedcall", sa.Boolean(), nullable=True),
        sa.Column("has_received_callback", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("signup_date", sa.DateTime(), nullable=True),
        sa.Column("sector", sa.String(length=50), nullable=True),
        sa.Column("circle_code", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["partner_id"],
            ["partner.id"],
        ),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_program",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.Column("preferred_time_slot", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "call_log",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("registration_id", sa.Integer(), nullable=True),
        sa.Column("program_sequence_id", sa.Integer(), nullable=True),
        sa.Column("content_version_id", sa.Integer(), nullable=True),
        sa.Column("call_sid", sa.Integer(), nullable=True),
        sa.Column("flow_run_uuid", sa.String(length=255), nullable=True),
        sa.Column("call_type", sa.String(length=50), nullable=True),
        sa.Column("scheduled_by", sa.String(length=100), nullable=True),
        sa.Column("user_phone_number", sa.String(length=50), nullable=False),
        sa.Column("system_phone_number", sa.String(length=50), nullable=True),
        sa.Column("circle", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("listen_seconds", sa.String(length=50), nullable=True),
        sa.Column("recording_url", sa.String(length=1000), nullable=True),
        sa.Column("dial_time", sa.DateTime(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("flow_category", sa.String(length=50), nullable=True),
        sa.Column("call_category", sa.String(length=50), nullable=True),
        sa.Column("parent_flow_run_uuid", sa.String(length=255), nullable=True),
        sa.Column("parent_flow_name", sa.String(length=255), nullable=True),
        sa.Column("flow_run_created_on", sa.DateTime(), nullable=True),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column("flow_name", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_version_id"],
            ["content_version.id"],
        ),
        sa.ForeignKeyConstraint(
            ["program_sequence_id"],
            ["program_sequence.id"],
        ),
        sa.ForeignKeyConstraint(
            ["registration_id"],
            ["registration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_custom_fields",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("registration_id", sa.Integer(), nullable=True),
        sa.Column("user_phone", sa.String(length=50), nullable=False),
        sa.Column("flow_run_uuid", sa.String(length=255), nullable=True),
        sa.Column("field_name", sa.String(length=255), nullable=False),
        sa.Column("field_value", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(
            ["registration_id"],
            ["registration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_group",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_phone", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("registration_id", sa.Integer(), nullable=True),
        sa.Column("group_name", sa.String(length=255), nullable=False),
        sa.Column("group_uuid", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(
            ["registration_id"],
            ["registration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_group")
    op.drop_table("user_custom_fields")
    op.drop_table("call_log")
    op.drop_table("user_program")
    op.drop_table("registration")
    op.drop_table("program_sequence")
    op.drop_table("program_module")
    op.drop_table("module_content")
    op.drop_table("ivr_prompt_response")
    op.drop_table("ivr_prompt_mapping")
    op.drop_table("user")
    op.drop_table("partner_system_phone")
    op.drop_table("module")
    op.drop_table("ivr_prompt")
    op.drop_table("content_version")
    op.drop_table("webhook_transaction_log")
    op.drop_table("system_phone")
    op.drop_table("program")
    op.drop_table("partner")
    op.drop_table("language")
    op.drop_table("ivr_callback_transaction_log")
    op.drop_table("content")
    op.drop_table("contact_fields_mapping")
    op.drop_table("call_log_event")
    op.drop_table("bigquery_jobs")
    # ### end Alembic commands ###
