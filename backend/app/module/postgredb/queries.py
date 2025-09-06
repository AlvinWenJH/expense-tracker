import os

timezone = os.getenv("TIME_ZONE", "Asia/Jakarta")

QUERY = {}

QUERY["CREATE_TRACKER_TABLE"] = """
CREATE TABLE IF NOT EXISTS tracker (
	id uuid NOT NULL,
	order_type text NOT NULL,
	description text NOT NULL,
	category text NOT NULL,
    price int NOT NULL,
    restaurant text NOT NULL,
    is_deleted boolean DEFAULT false NOT NULL,
    purchased_at timestamptz DEFAULT now() NOT NULL,
    registered_at timestamptz DEFAULT now() NOT NULL,
    CONSTRAINT tracker_pkey PRIMARY KEY (id)
);

COMMENT ON COLUMN tracker.order_type IS 'Grabfood, Gofood, Shopeefood, Offline';
COMMENT ON COLUMN tracker.description IS 'items details';
COMMENT ON COLUMN tracker.category IS 'Food, Beverage, Snack';
COMMENT ON COLUMN tracker.restaurant IS 'Name of the store/restaurant';
COMMENT ON COLUMN tracker.price IS 'Price of the item';
COMMENT ON COLUMN tracker.purchased_at Is 'Date and time when the item is purchased if the receipt includes it. If not use the current time';
COMMENT ON COLUMN tracker.registered_at Is 'Date and time when the item is registered in the database';
"""
