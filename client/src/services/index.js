import { post, get, fileUpload } from "./base";


function postData(url, data, eventListner, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    post(url, data).then(data => eventListner(data)).catch(error => errorHandler(error));
}

function getData(url, eventListner, queryParams = null, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    get(url, queryParams).then(data => eventListner(data)).catch(error => errorHandler(error))
}

function uploadFile(url, fileData, eventListner, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    fileUpload(url, fileData).then(data => eventListner(data)).catch(error => errorHandler(data))
}


export { postData, getData, uploadFile };