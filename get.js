'use strict';

const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const request = require('request');

// Loaded from environment vars
const recaptchaSecret = process.env.GOOGLE_RECAPTCHA_TOKEN;

// Required in responses for CORS support to work
const headers = {'Access-Control-Allow-Origin': '*'};

module.exports.thoughts = (event, context, callback) => {
  
  const validationData = {
    url: 'https://www.google.com/recaptcha/api/siteverify?secret=' + 
    recaptchaSecret + "&response=" + event.body.captcha,
    method: 'POST'
  };

  const params = {
    TableName: process.env.DYNAMODB_TABLE,
    Key: {
      id: (Math.floor(Math.random() * 66) + 1).toString(),
    },
  };

  request(validationData, function(error, response, body) {
    const parsedBody = JSON.parse(body)

    if (error || response.statusCode !== 200){

      const recaptchaErrResponse = {
        headers: headers,
        statusCode: 500,
        body: JSON.stringify({
          status: 'fail',
          message: 'Error attempting to validate recaptcha.',
          error: error || response.statusCode
        }),
      };

      return callback(null, recaptchaErrResponse);
    } else if (parsedBody.success === false) {
      
      const recaptchaFailedErrResponse = {
        headers: headers,
        statusCode: 200,
        body: JSON.stringify({
          status: 'fail',
          message: 'Captcha validation failed. Refresh the page & try again!',
        })
      };
      
      return callback(null, recaptchaFailedErrResponse);
    } else if (parsedBody.success === true) {
      // fetch item from the database
      dynamoDb.get(params, (error, result) => {
        // handle potential errors
        if (error) {
          console.error(error);
          callback(new Error('Couldn\'t fetch the item.'));
          return;
        }

        // create a response
        const response = {
          status: 'success',
          headers: headers,
          statusCode: 200,
          body: JSON.stringify(result.Item),
        };
        callback(null, response);
      })
    };
  });
};