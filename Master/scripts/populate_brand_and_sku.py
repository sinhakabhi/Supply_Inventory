import csv
from Inventory.models import Brand, SKUCatalogue


brands_csv_path = 'Inventory\Brands - Sheet1.csv'
sku_csv_path ='Inventory\PO Sample data - Sheet1.csv'

def run():
    # with open(brands_csv_path, 'r') as file:
    # # Skip the header line if it exists
    #     header = next(file, None)

    #     # Assuming 'BrandName' is the column containing the brand names
    #     for line in file:
    #         # Remove leading and trailing whitespaces
    #         brand_name = line.strip()
    #         print(brand_name)

    #         Brand.objects.update_or_create(name=brand_name)

    with open(sku_csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            brand_obj = Brand.objects.get(name=row['Brand Name (Mandatory)'])
            SKUCatalogue.objects.update_or_create(
                sku_name = row['Product Name'],
                hsn_code = row['HSN CODES'],
                ean_code = row['EAN CODES'],
                mrp = row['MRP'],
                brand=brand_obj,
                unit_price = 1000
            )
            # print(float(row['MRP']))
