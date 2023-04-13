from typing import Optional, Union
from fastapi import FastAPI, Request, params, Depends, Query
import uvicorn
from sqlmodel import select, create_engine, Session, SQLModel
import pydantic
from fast_lookup import Lookup
from models import SolarPanel

app = FastAPI()
sql_url = f'sqlite:///database.db'
engine = create_engine(sql_url)
session = Session(bind=engine)


def helper_function(query_list):
    for q in query_list:
        key, value = q
        try:
            field, oper = key.split('__')
        except:
            field = key
            oper = 'eq'
        yield field, oper, value


class CommonParams:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, Query(value))
    #     b: int = Query(*SolarPanel.__fields__.keys(), description="Using query changes nothing"),
    #     a: int = Query(5, description="This description shows up"),




#s = SolarPanelParams(**SolarPanel.__fields__.keys())
#print(s)
#c = CommonParams(**SolarPanel.__fields__)
#print(c)


class SolarPanelParams(pydantic.BaseModel):
    pass


fields = SolarPanel.__fields__.items()
for f in fields:
    first, second = f
    second.required = False
    SolarPanelParams.__fields__.update({first: second})

# print(SolarPanel.__dict__)
# print('--------------------------------')
# print(SolarPanelParams.__dict__)


def properties(**kwargs):
    def paramsfunc(params):
        params = {}
        for key, value in kwargs.items():
            params.update({key: value})
        return params
    return paramsfunc(params)

p = properties(**SolarPanelParams.__fields__)


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content


def class_factory():

    def init(self, color):
        self.color = color

    def getColor(self):
        return self.color

    return type('Apple', (object,), {
        '__init__': init,
        'getColor': getColor,

    })

test = class_factory()

def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


print(common_parameters.__dict__)


@app.get('/panels', tags=['SunnyLife'])
def panels_search(r: Request, commons: dict = Depends(common_parameters)
                   ):
    panels = select(SolarPanel)
    panels = Lookup(SolarPanel, panels)
    #print(r.query_params.keys())
    params = helper_function(r.query_params.multi_items())
    for param in params:
        panels = panels.perform_lookup(*param)

    return session.exec(panels.inst).all()


if __name__ == "__main__":
    #SQLModel.metadata.create_all(engine)
    uvicorn.run('main:app', host="localhost", port=8002, reload=True)
