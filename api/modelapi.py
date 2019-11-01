from wsgiref.simple_server import make_server

import falcon
import json
import numpy as np
import trainer.datemodel as datemodel
import api.middleware as middleware

class ModelServer:
    model = None
    configuration = None
    params = None
    human = None    
    def __init__(self):
        pass
    def load_config(self,configfile,weightsfile):
        f=open(configfile)
        self.configuration=json.load(f)
        f.close()
        self.params=self.configuration['config']
        self.human=self.configuration['human']
        self.machine = self.configuration['machine']
        self.inv_machine = {int(v):k for k,v in self.machine.items()}
        mw = datemodel.ModelWrapper()
        self.model = mw.create_model(self.params['Tx'],self.params['Ty'],self.params['n_a'],self.params['n_s'],len(self.human),len(self.machine))
        self.model.load_weights(weightsfile)

    @falcon.before(middleware.max_body(128*1024))
    def on_post(self,req,resp):
        strings = req.media.get('dates',[])
        Xoh,Xints,s0,c0 = self.createInputs(strings)
        Yoh = self.model.predict([Xoh,s0,c0])
        Ystrings = self.decodeOutputs(Yoh)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"result":"OK","data": Ystrings})

    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'result':'ok'})

    def createInputs(self,strings):
        Xints,Xoh = datemodel.encode_strings(strings,self.params['Tx'],self.human)
        s0 = np.zeros((len(strings),self.params['n_s']))
        c0 = np.zeros((len(strings),self.params['n_s']))
        return Xoh,Xints,s0,c0

    def decodeOutputs(self,Yoh):
        Yoh = np.array(Yoh).swapaxes(0,1)
        Ystring = datemodel.decode_strings(Yoh,self.inv_machine)
        return Ystring



app = falcon.API(middleware=[middleware.RequireJSON()])
modserver = ModelServer()
modserver.load_config('config.json','dataweights.h5')


app.add_route('/datereader',modserver)

if __name__ == '__main__' :
    with make_server('',8080,app) as httpd:
        print("Started server on port 8080")
        httpd.serve_forever()