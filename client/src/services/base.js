
export function post(url, body, contentType = "application/json") {
    var url = new URL(API_URL + url);
    return call(url, body, 'POST', contentType);
}

export function get(url, queryParams) {
    var url = new URL(API_URL + url);
    if (queryParams != null) {
        url.search = new URLSearchParams(queryParams);
    }
    return call(url, null, 'GET');
}

export function fileUpload(url, fileData) {
    var url = new URL(API_URL + url);
    return call(url, fileData, 'POST');
}

async function call(url, body, method, contentType = null) {
    // Default options are marked with *
    var api_data = {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    }
    if (contentType != null) {
        api_data['headers'] = {
            'Content-Type': contentType
        }
    }
    if (method != 'GET') {
        if (contentType == "application/json") {
            api_data['body'] = JSON.stringify(body);
        }
        else {
            api_data['body'] = body;
        }
    }
    const response = await fetch(url, api_data);
    return {
        status: response.status
        , data: await response.json()
    }// parses JSON response into native JavaScript objects
}