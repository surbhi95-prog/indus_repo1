from django.urls import path

from apps.inventory.views.category_views import (
    CategoryListCreateView,
    CategoryDetailView,
)

from apps.inventory.views.uom_views import (
    UOMListCreateView,
    UOMDetailView,
)

from apps.inventory.views.item_views import (
    ItemListCreateView,
    ItemDetailView,
)

from apps.inventory.views.warehouse_views import (
    WarehouseListCreateView,
    WarehouseDetailView,
)

from apps.inventory.views.storage_location_views import (
    StorageLocationListCreateView,
    StorageLocationDetailView,
)

from apps.inventory.views.batch_views import (
    BatchListCreateView,
    BatchDetailView,
)

from apps.inventory.views.stock_views import (
    StockListView,
    StockDetailView,
    ReceiveStockView,
    IssueStockView,
    TransferStockView,
    AdjustStockView,
)

from apps.inventory.views.stock_movement_views import (
    StockMovementListView,
    StockMovementDetailView,
    ItemStockHistoryView,
    BatchStockHistoryView,
)
from apps.inventory.views.report_views import (
    StockSummaryReportView,
    StockReportView,
)

urlpatterns = [

    # ==========================================================
    # CATEGORY
    # ==========================================================

    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),

    path(
        "categories/<uuid:category_id>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),


    # ==========================================================
    # UOM
    # ==========================================================

    path(
        "uoms/",
        UOMListCreateView.as_view(),
        name="uom-list-create",
    ),

    path(
        "uoms/<uuid:uom_id>/",
        UOMDetailView.as_view(),
        name="uom-detail",
    ),


    # ==========================================================
    # ITEMS
    # ==========================================================

    path(
        "items/",
        ItemListCreateView.as_view(),
        name="item-list-create",
    ),

    path(
        "items/<uuid:item_id>/",
        ItemDetailView.as_view(),
        name="item-detail",
    ),


    # ==========================================================
    # WAREHOUSE
    # ==========================================================

    path(
        "warehouses/",
        WarehouseListCreateView.as_view(),
        name="warehouse-list-create",
    ),

    path(
        "warehouses/<uuid:warehouse_id>/",
        WarehouseDetailView.as_view(),
        name="warehouse-detail",
    ),


    # ==========================================================
    # STORAGE LOCATIONS
    # ==========================================================

    path(
        "storage-locations/",
        StorageLocationListCreateView.as_view(),
        name="storage-location-list-create",
    ),

    path(
        "storage-locations/<uuid:location_id>/",
        StorageLocationDetailView.as_view(),
        name="storage-location-detail",
    ),


    # ==========================================================
    # BATCHES
    # ==========================================================

    path(
        "batches/",
        BatchListCreateView.as_view(),
        name="batch-list-create",
    ),

    path(
        "batches/<uuid:batch_id>/",
        BatchDetailView.as_view(),
        name="batch-detail",
    ),


    # ==========================================================
    # STOCK
    # ==========================================================

    # Current stock
    path(
        "stock/",
        StockListView.as_view(),
        name="stock-list",
    ),

    # Single stock record
    path(
        "stock/<uuid:stock_id>/",
        StockDetailView.as_view(),
        name="stock-detail",
    ),

    # Receive stock
    path(
        "stock/receive/",
        ReceiveStockView.as_view(),
        name="stock-receive",
    ),

    # Issue stock
    path(
        "stock/issue/",
        IssueStockView.as_view(),
        name="stock-issue",
    ),

    # Transfer stock
    path(
        "stock/transfer/",
        TransferStockView.as_view(),
        name="stock-transfer",
    ),

    # Stock adjustment
    path(
        "stock/adjustment/",
        AdjustStockView.as_view(),
        name="stock-adjust",
    ),


    # ==========================================================
    # STOCK MOVEMENTS
    # ==========================================================

    path(
        "stock-movements/",
        StockMovementListView.as_view(),
        name="stock-movement-list",
    ),

    path(
        "stock-movements/<uuid:movement_id>/",
        StockMovementDetailView.as_view(),
        name="stock-movement-detail",
    ),


    # ==========================================================
    # STOCK HISTORY
    # ==========================================================

    path(
        "items/<uuid:item_id>/stock-history/",
        ItemStockHistoryView.as_view(),
        name="item-stock-history",
    ),

    path(
        "batches/<uuid:batch_id>/stock-history/",
        BatchStockHistoryView.as_view(),
        name="batch-stock-history",
    ),

     path(
        "reports/stock-summary/",
        StockSummaryReportView.as_view(),
        name="stock-summary-report"
    ),

    path(
        "reports/",
        StockReportView.as_view(),
        name="stock-report"
    ),
]