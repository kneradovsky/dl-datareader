const Telegraf = require("telegraf");
const http = require('http');

class MyResponse {
    constructor() {
        this.headersSent = true
        this.endCallback = null
    }
    end(data,encoding,callback) {
        this.endCallback(data);
        callback();
    }
}

const token = "638384571:AAELE4bPhevDwsiO5cesKme0dPEu7I8OGM0"
const functionURL="https://functions.yandexcloud.net/d4e600h16kpk1of6r83r"
const bot = new Telegraf(token)
bot.telegram.setWebhook(functionURL)

bot.help((ctx) => ctx.reply("Я нейродатабот. Отправь мне дату на русском, украинском или белорусском и я верну ее в формате Год-Месяц-День "))
bot.start((ctx) => ctx.reply("Я нейродатабот. Отправь мне дату на русском, украинском или белорусском и я верну ее в формате Год-Месяц-День "))
bot.on('text', (ctx) => {
    if(ctx.message.text.indexOf("start")!=-1 || 
       ctx.message.text.indexOf("help")!=-1 || 
       ctx.message.text.toLowerCase().indexOf("помо")!=-1) 
        return ctx.reply("Я нейродатабот. Отправь мне дату на русском, украинском или белорусском и я верну ее в формате Год-Месяц-День ")
    const date = ctx.message.text
    body = JSON.stringify({"dates":[date]})
    httpOptions = {
        "host": "84.201.173.58",
        "port": 8080,
        "path": "/datereader",
        "method": "POST",
        "headers": {
            "Content-type": "application/json",
            "Content-length": Buffer.byteLength(body)
        } 
    }
    responseBody = ""
    const req = http.request(httpOptions,(res) => {
        res.setEncoding('utf-8')
        if(res.statusCode>399) ctx.reply(`ошибка: ${res.statusMessage}`)
        else {
            res.on('data',(chunk)=>responseBody+=chunk)
            res.on('end',() => {
                respData = JSON.parse(responseBody)
                ctx.reply(respData.data[0])
            })
            res.on('error',(err) => ctx.reply(JSON.stringify(err)))
        }
    })
    req.write(body)
    req.end()
})

exports.loghandler = async function(event,context) {
    reqbodystr = event.body
    reqbody = JSON.parse(reqbodystr)
    return {
        'statusCode' : 200,
        'isBase64Encoded': false,
        'body' : JSON.stringify([reqbody.text])
    }
}

exports.handler = async function(event,context) {
    if(event.httpMethod!="POST") 
     return {
            'statusCode': 405,
            'isBase64Encoded' : false,
            'body' : 'invalid method. Only post allowed'
        }
        
    const updatestr = event.body
    const update = JSON.parse(updatestr)
       
    pr = new Promise((resolve,reject) => {
        resp = new MyResponse()
        resp.headersSent=true;
        resp.endCallback = (data) => {
            ret = {
                'statusCode': 200,
                'isBase64Encoded' : false,
                'headers': {
                    'Content-type' : 'application/json'
                },
                'body' : data
            }
            resolve(ret)
        }
        bot.handleUpdate(update,resp)  
    })
    retval = await pr
    console.log("all done")
    console.log(retval.statusCode)
    return retval
}


