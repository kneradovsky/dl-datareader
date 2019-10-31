from wsgiref.simple_server import make_server

import falcon
import json
import numpy as np
import trainer.datemodel as datemodel

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
        mw = datamodel.ModelWrapper()
        model = mw.create_model(self.params['Tx'],self.params['Ty'],self.params['n_a'],self.params['n_s'],len(self.human),len(self.machine))
        model.load_weights(weightsfile)

    def on_post(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"result":"OK"})

    def createInputs(self,string):
        Xints,Xoh = datamodel.encode_strings(string,self.params['Tx'],self.human)
        s0 = np.zeros((1,self.params['n_s']))
        c0 = np.zeros((1,self.params['n_s']))
        return Xoh,Xints,s0,c0

    def decodeOutputs(Yoh):
        Yoh = np.array(Yoh).swapaxes(0,1)
        Ystring = datamodel.decode_strings(Yoh,self.inv_machine)
        return Ystring

app = falcon.API()
modserver = ModelServer()
modserver.load_config('config.json','dataweight.h5')


app.add_route('/datareader',modserver)

if __name__ == '__main__' :
    with make_server('',8080,app) as httpd:
        print("Started server on port 8080")
        httpd.serve_forever()