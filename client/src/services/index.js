import { post, get, fileUpload } from "./base";


function postData(url, data, eventListner, eventErrorHandler = null, errorHandler = null) {
    callAPI(post, url, data, eventListner, eventErrorHandler, errorHandler);
}

function getData(url, queryParams, eventListner, eventErrorHandler = null, errorHandler = null) {
    callAPI(get, url, queryParams, eventListner, eventErrorHandler, errorHandler);
}

function uploadFile(url, fileData, eventListner, eventErrorHandler = null, errorHandler = null) {
    callAPI(fileUpload, url, fileData, eventListner, eventErrorHandler, errorHandler);
}

function callAPI(apiMethod, url, requestData, eventListner, eventErrorHandler, errorHandler = null) {
    if (eventErrorHandler == null) {
        eventErrorHandler = eventListner;
    }
    if (errorHandler == null) {
        errorHandler = error => console.error(error);
    }
    apiMethod(url, requestData).then(data => { if (data.status == 200) { eventListner(data.data) } else { eventErrorHandler(data.data) } }).catch(error => errorHandler(error))
}

export { postData, getData, uploadFile };