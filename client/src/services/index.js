import { post, get, fileUpload } from "./base";


function postData(url, data, eventListner, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    post(url, data).then(data => { if (data.status == 200) { eventListner(data.data) } else { errorHandler(data.data) } }).catch(error => console.error(error));
}

function getData(url, eventListner, queryParams = null, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    get(url, queryParams).then(data => { if (data.status == 200) { eventListner(data.data) } else { errorHandler(data.data) } }).catch(error => console.error(error))
}

function uploadFile(url, fileData, eventListner, errorHandler = null) {
    if (errorHandler == null) {
        errorHandler = eventListner;
    }
    fileUpload(url, fileData).then(data => { if (data.status == 200) { eventListner(data.data) } else { errorHandler(data.data) } }).catch(error => console.error(error))
}


export { postData, getData, uploadFile };