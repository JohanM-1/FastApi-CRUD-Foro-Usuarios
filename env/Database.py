from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

engine = create_async_engine(
        "mysql+aiomysql://root:@localhost/Proyectomascotasv3",
        echo=True,
    )

async_session = async_sessionmaker(engine, expire_on_commit=False)