import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse, FileResponse, PlainTextResponse
import openai
openai.api_key = "sk-aaa"


app = FastAPI()
# app.mount("/public", StaticFiles(directory="public"), name="public")

# list engines
# print(openai.Engine.list())

# 文本模型：text-davinci-001、text-davinci-002、text-davinci-003
# 代码模型：code-davinci-002


@app.get("/")
def index():
    return FileResponse("public/index.html")


@app.post("/chat")
def chat(prompt: str = Body(embed=True)):
    try:
        def iterData():
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5,
                top_p=1,
                n=1,
                stream=True
            )
            yield from map(lambda x: x.choices[0].text, completion)
            # yield from map(str, list(prompt+"中文测试test\n<br> ## 顿阿三sssa请312213k"*5))
        return StreamingResponse(iterData(), media_type="stream/text")
    except Exception as e:
        return PlainTextResponse(str(e), status_code=500)


if __name__ == '__main__':
    # uvicorn.run(app='OpenAiChat:app', host="127.0.0.1", port=8080, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8080)
