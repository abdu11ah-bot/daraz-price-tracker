import logging
from app.webscraper import Webscraper
from app.database import Session
from app.model import Product


def get_old_price(name):
    session = Session()
    p = session.query(Product).filter(Product.name == name).first()
    session.close()
    return p.price if p else None


def save_price(url1, name1, price1):
    session = Session()
    p = session.query(Product).filter(Product.url == url1).first()
    if p:
        p.price = price1
    else:
        p = Product(name=name1, price=price1, url=url1)
        session.add(p)
    session.commit()
    session.close()
    logging.info(f"Saved — Name: {name1} | Price: {price1}")


def compare_price(name, new_price, url):
    old_price = get_old_price(name)
    new_price = float(new_price)
    if old_price is None:
        save_price(url, name, new_price)
        return [str(name), new_price, new_price]  # [name, new_price, old_price]
    else:
        old_price = float(old_price)  # type: ignore
        if new_price != old_price:
            save_price(url, name, new_price)
        return [str(name), new_price, old_price]


def get_all_product_data():
    session = Session()
    products = session.query(Product).all()
    session.close()

    results = []

    for p in products:
        url = p.url
        logging.info(f"Tracking URL: {url}")

        result = Webscraper(url)
        if result is None:
            continue

        name, price = result
        price = float(price)

        old_price_raw = get_old_price(name)
        name, new_price, old_price = compare_price(name, price, url)

        difference = round(new_price - old_price, 2)

        if old_price_raw is None:
            status = "new"
        elif new_price > old_price:
            status = "increased"
        elif new_price < old_price:
            status = "decreased"
        else:
            status = "no_change"

        results.append(
            {
                "status": status,
                "name": name,
                "url": url,
                "new_price": new_price,
                "last_price": old_price,
                "difference": difference,
                "percent_change": round((difference / old_price) * 100, 2)
                if old_price
                else 0,
            }
        )

    return results


def delete_product_by_url(url):
    session = Session()
    p = session.query(Product).filter(Product.url == url).first()
    if p:
        session.delete(p)
        session.commit()
        session.close()
        return True
    session.close()
    return False


def delete_product_by_id(product_id):
    session = Session()
    p = session.query(Product).filter(Product.id == product_id).first()
    if p:
        session.delete(p)
        session.commit()
        session.close()
        return True
    session.close()
    return False
