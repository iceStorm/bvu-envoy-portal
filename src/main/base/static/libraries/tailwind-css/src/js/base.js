/**
 * Initializing the App. Also run initial configs.
 */
const app = new App({
    backendEndpoint: '/',
    scrollTopButton: {
        visible: false,
    }
});



/**
 *  The showToast function.
 */
function showToast(text, type, duration=5000) {
    // console.log('showing toast:', text);

    $.message({
        type: type,
        text: text,
        duration: duration,
        position: 'bottom-center',
    });
}


/*
 * Setting ajax navigating for a tags that don't have the '' class.
 */
setATagNavigate();
function setATagNavigate() {
    $('a:not(.not-ajax)').each(function(index, elem) {
        $(this).unbind('click').click((e) => {
            e.preventDefault();

            const href = $(this).attr('href');
            navigateTo(href);
        });
    });
}
function ajaxNavigate(e) {
    e.preventDefault();

    const href = e.target.href;
    navigateTo(href);
}



/**
 * Handling on user pressed the Back button on the browser, or even going back by code.
 */
$(window).on("popstate", function (e) {
    console.log('\back pressed:', location.href);
    navigateTo(location.href);

    /*if (e.originalEvent.state !== null) {
        loadAjaxContent(location.href);
    }*/
});


/*
 * Navigating to the desired path by ajax calling.
 */
function navigateTo(path) {
    axios.get(path)
        .then(res => {
            replaceContent(res);
        })
        .catch(err => {
            console.log(err);
        });
}


/**
 * Replacing the #main's innerHTML.
 */
function replaceContent(axiosResponse) {
    const html = axiosResponse.data;
    const path = axiosResponse.request.responseURL;

    // expression: $.parseHTML(data, context = document, keepScripts = false)
    const ajaxContent = $('<div>').append($.parseHTML(html, document, true));
    // console.log('The whole content:', html);
    // console.log('The main content:', ajaxContent.find('#main').html());


    //  replacing html
    $('#main').html(ajaxContent.find('#main').html());
    $('#nav').html(ajaxContent.find('#nav').html());


    //  changing the url bar's content
    window.history.pushState('', '', `${path}`);


    // re-set for new-in a tags
    app.initTippy();
    setATagNavigate();
    setSubmit();
}


/**
 * Setting ajax submit for forms that has the 'ajax' class.
 */
setSubmit();
function setSubmit() {
    $('form.ajax').each(function(index, elem) {
        $(this).submit((e) => {
            e.preventDefault();


            // getting query params
            let query_params = {};
            if (e.target.method == 'get') {
                $(e.target).find('input').each(function() {
                    if (this.type != 'submit')
                    query_params[this.name] = this.value;
                });
            }


            axios.request({
                method: e.target.method,
                url: e.target.action,
                data: e.target.method == 'post' ? new FormData(e.target) : null,
                params: query_params,
            })
                .then(res => {
                    replaceContent(res);
                })
                .catch(err => {
                    showToast(err.response.data.message, 'error');
                    console.log(err);
                });
        });
    });
}


/**
 * Getting Browser URL's query parameters
 */
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
