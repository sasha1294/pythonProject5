from oauth_2.src.conf.Api_conf import app
from oauth_2.src.models.user.app import router
import uvicorn

if __name__ == "__main__":
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=8000)




