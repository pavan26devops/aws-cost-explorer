#!/usr/bin/env groovy

@Library(value = 'notifications-lib', changelog = false) _

pipeline {
  agent any
  triggers{
    cron('0 7 4 * *')
  }
  stages {
    stage ('Build') {
      steps {
        sendNotifications('STARTED', '#devops-cron')
        sh '''
          #!/bin/sh
          set -e
          cd ec2-cost-explorer
          docker build -t tools-ec2-cost-explorer .
        '''
      }
    }
    stage ('Run Cost Explorer') {
      steps {
        sh '''
          #!/bin/sh
          set -e
          docker run tools-ec2-cost-explorer
        '''
      }
    }
  }
  post {
    always {
      sendNotifications(currentBuild.result, '#devops-cron')
    }
  }
}
