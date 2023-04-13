import random

from sqlmodel import Session

from main import engine
from models import SolarPanel

brands = ('Samsung', 'LG', 'Panasonic')


def generate_panel_props():
    price = random.randint(1000, 20000)
    brand = random.choice(brands)
    power_output = random.randint(1, 5)*price/100
    current = random.choice((12, 24))
    warranty = random.randint(3, 25)
    weight = random.randint(3, 30)/10*power_output
    height = random.randint(30, 250)
    monocrystal = bool(random.randint(0, 1))
    return [price, brand, power_output, current, warranty, weight, height, monocrystal]


def create_panel():
    price, brand, power_output, current, \
    warranty, weight, height, monocrystal = generate_panel_props()
    panel = SolarPanel(price=price, brand=brand, power_output=power_output,
                       current=current, warranty_years=warranty, weight=weight,
                       height=height, monocrystal=monocrystal)
    return panel


def create_panel_db():
    panels = [create_panel() for x in range(1500)]
    with Session(engine) as session:
        session.add_all(panels)
        session.commit()

create_panel_db()