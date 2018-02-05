from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
import facebook

from mainapp.forms import UserForm
from mainapp.models import UserPage, BusinessAccountDetails
from mainapp import utils
from datetime import date
import requests


# Create your views here.
class WatsonDashboard(View):
    def get(self, request):
        return render(request, 'ibm_watson/index.html')

    def post(self, request):
      type_ = request.POST['optionsRadios']
      text = request.POST['text']
      if type_ == 'tone':
        headers = {'content-type': 'text/plain;charset=utf-8'}
        payload = text
        res = requests.post(url='https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21',
            data= payload,
            headers= headers,
            auth = ('14bd2691-f7a4-434a-b56b-0916f676b7d1', 'KlF71h0J4EYI'))
        # tone = tone_analyzer.tone(text)
        tone = res.json()
        print("tone", tone)
        if not tone['document_tone']['tones']:
          html_data = '''
              <div class="row">
                <div class="card">
                  <div class="card-body">
                              <h5 class="card-title alert alert-danger">Error</h5>
                              <p class="card-text">{0}</p>
                            </div>
                </div>
              </div>
          '''.format('Please provide a valid Input!')
          return HttpResponse(html_data)

        html_data = '''
            <div class="row">
                <div class="col-sm-12">
                  <div class="card">
                    <div class="card-body">
                      <h5 class="card-title alert alert-success">Tone Insights</h5>
                      <p class="card-text"></p>
        '''
        for sentence in tone['sentences_tone']:
          for sentence_tone in sentence['tones']:
            html_data += '''
              <h3>{2}</h3>
              <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: {0}% ;" aria-valuenow="{0}" aria-valuemin="0" aria-valuemax="100">{1} {0}%</div>
              </div>

          '''.format(int(sentence_tone['score'] * 100), sentence['text'], sentence_tone['tone_name'])
        html_data += '''
              </div>
            </div>
            </div>
          </div>
        '''
        return HttpResponse(html_data)

      # curl -X POST --user "afac5070-e852-4695-ad00-a576bf09af5a":"mE7wE5vQPZJd" --header "Content-Type: text/plain;charset=utf-8" --data-binary "@/home/laptop30/Downloads/profile.json" "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13"
      headers = {'content-type': 'text/plain;charset=utf-8'}
      user = {"afac5070-e852-4695-ad00-a576bf09af5a":"mE7wE5vQPZJd"}
      payload = text
      res = requests.post(url='https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13',
          data= payload,
          headers= headers,
          auth = ('afac5070-e852-4695-ad00-a576bf09af5a', 'mE7wE5vQPZJd'))
      datap = res.json()
      if 'code' in datap:
        html_data = '''
          <div class="row">
            <div class="card">
              <div class="card-body">
                          <h5 class="card-title alert alert-danger">Error</h5>
                          <p class="card-text">{0}</p>
                        </div>
            </div>
          </div>
        '''.format(datap['error'])
        return HttpResponse(html_data)
      a = int(datap['personality'][0]['percentile'] * 100)
      b = int(datap['personality'][1]['percentile'] * 100)
      c = int(datap['personality'][2]['percentile'] * 100)
      d = int(datap['personality'][3]['percentile'] * 100)
      e = int(datap['personality'][4]['percentile'] * 100)
      word_count = datap['word_count']

      html_data = '''
        <div class="row">
                    <div class="col-sm-12">
                      <div class="card">
                        <div class="card-body">
                          <h5 class="card-title alert alert-success">Personality Insights</h5>
                          <p class="card-text"></p>
                          <p>Word Count {5}</p>

                          <h3>Openness</h3>
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {0}% ;" aria-valuenow="{0}" aria-valuemin="0" aria-valuemax="100">{0} %</div>
                          </div>

                          <h3>Conscientiousness</h3>
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {1}%;" aria-valuenow="{1}" aria-valuemin="0" aria-valuemax="100">{1}%</div>
                          </div>
                          <h3>Extraversion</h3>
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {2}%;" aria-valuenow="{2}" aria-valuemin="0" aria-valuemax="100">{2}%</div>
                          </div>

                          <h3>Agreeableness</h3>
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {3}%;" aria-valuenow="{3}" aria-valuemin="0" aria-valuemax="100">{3}%</div>
                          </div>
                          <h3>Emotional range</h3>
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {4}%;" aria-valuenow="{4}" aria-valuemin="0" aria-valuemax="100">{4}%</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
        '''.format(a,b,c,d,e,word_count)
      return HttpResponse(html_data)

class WatsonPersonality(View):
    def get(self, request):
        return render(request, 'ibm_watson/personality.html')