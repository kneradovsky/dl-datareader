const Telegraf = require('telegraf')
const http = require('http')
//const express = require('express')

//const app = express()

const bot_token ="638384571:AAELE4bPhevDwsiO5cesKme0dPEu7I8OGM0";
const webhookurl = "https://us-central1-deeplearning-cc7ec.cloudfunctions.net/dmbot";

const bot = new Telegraf(bot_token);
bot.telegram.setWebhook(webhookurl)
//app.use(bot.webhookCallback('/'))


exports.dmbot = (req,res) => bot.handleUpdate(req.body,res)

//bot.hears('test',(ctx)=>ctx.reply('test passed'))
bot.help((ctx) => ctx.reply("Я нейродатабот. Отправь мне дату на русском, украинском или белорусском и я верну ее в формате Год-Месяц-День "))
bot.start((ctx) => ctx.reply("Я нейродатабот. Отправь мне дату на русском, украинском или белорусском и я верну ее в формате Год-Месяц-День "))
bot.on('text', (ctx) => {
    const date = ctx.message.text
    body = JSON.stringify([date])
    httpOptions = {
        "host": "10.128.0.6",
        "port": 80,
        "path": "/datereader",
        "method": "POST",
        "headers": {
            "Content-type": "application/json",
            "Content-length": body.length
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
                ctx.reply(respData[0])
            })
            res.on('error',(err) => ctx.reply(JSON.stringify(err)))
        }
    })
    req.write(body)
    req.end()
})
