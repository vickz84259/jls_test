DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS locations;

CREATE TABLE products (
    core_number TEXT PRIMARY KEY NOT NULL,
    internal_title TEXT NOT NULL,
    vendor TEXT NOT NULL,
    vendor_title TEXT,
    vendor_sku TEXT,
    backup_vendor TEXT,
    backup_vendor_sku TEXT,
    restockable INTEGER CHECK (restockable IN (0, 1)),
    vendor_order_unit TEXT,
    vendor_case_pack INTEGER CHECK (vendor_case_pack >= 0),
    moq INTEGER CHECK (moq >= 0),
    buffer_days INTEGER NOT NULL CHECK (buffer_days >= 0),
    minimum_level TEXT,
    product_url TEXT,
    next_order_note TEXT,
    case_pack INTEGER CHECK (case_pack >= 0),
    pieces_per_internal INTEGER CHECK (pieces_per_internal >= 0),
    boxes_per_case INTEGER CHECK (boxes_per_case >= 0),
    tags_info TEXT,
    tag_1 TEXT,
    tag_2 TEXT,
    tag_3 TEXT,
    tag_4 TEXT,
    hazmat INTEGER CHECK (hazmat IN (0, 1)),
    active INTEGER CHECK (active IN (0, 1)),
    ignore_until TEXT,
    notes TEXT
);

CREATE TABLE locations (
    warehouse TEXT NOT NULL,
    product_code TEXT NOT NULL,
    location TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (warehouse, product_code, location)
);
