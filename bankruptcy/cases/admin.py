from django.contrib import admin
from .models import Case, DocketEntry, Document

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ["name", "recap_id", "date_filed", "jurisdiction", "chapter"]
    search_fields = ["name", "chapter", "jurisdiction", "recap_id", "pacer_id"]
    list_per_page = 25

@admin.register(DocketEntry)
class DocketEntryAdmin(admin.ModelAdmin):
    list_display = ["recap_id", "case", "date_filed"]
    search_fields = ["recap_id", "description"]
    raw_id_fields = ["case"]
    list_per_page = 25

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["recap_id", "pacer_id", "doc_type", "is_available"]
    search_fields = ["description", "text", "pacer_id"]
    raw_id_fields = ["docket_entry"]
    list_per_page = 25