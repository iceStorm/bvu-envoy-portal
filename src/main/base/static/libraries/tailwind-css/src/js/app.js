'use strict';


class App {

    constructor({
        backendEndpoint = '/',
        scrollTopButton = {
            visible: true,
            offset: 200,
        }
    } = {}) {
        this.backendEndpoint = backendEndpoint;
        this.scrollTopButton = scrollTopButton;

        this.initNProgress();
        this.initTippy();

        this.setAxiosResponseInterceptor();

        if (this.scrollTopButton?.visible) {
            this.setupScrollTopButton();
        }
    }



    initNProgress() {
        /**
         * Initializing the progressbar.
         */
        loadProgressBar({
            speed: 450,
            trickleRate: 0.02,
            trickleSpeed: 1750,
            showSpinner: false,
        });
    }

    initTippy() {
        tippy('[data-tippy-content]');
    }

    initAxios() {
        // setting the baseURL for backend API calls
        axios.defaults.baseURL = this.backendEndpoint;
        axios.defaults.withCredentials = true;

        this.setAxiosResponseInterceptor();
    }

    setupScrollTopButton() {
        console.log(this.scrollTopButton);
    }

    setAxiosResponseInterceptor() {
        //  intercepting response to handle errors from the server or even on the client (network error..).
        axios.interceptors.response.use(
            res => {
                return res;
            },
            err => {
                console.log('axios error response:', err.response.status);
                // console.log('error data:', err.response);


                // getting error message from the server
                const theErrorMessage = err.response?.data?.message;

                switch (err.response.status) {
                    case 400: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Bad request! Please check your request data.',
                            position: 'bottom-center',
                        });
            
                        break;
                    }

                    case 401: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Not authenticated. Please login first!',
                            position: 'bottom-center',
                        });
            
                        break;
                    }
            
                    case 403: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Forbidden, please return!',
                            position: 'bottom-center',
                        });
            
                        break;
                    }
            
                    case 404: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Resource not found!',
                            position: 'bottom-center',
                        });
            
                        break;
                    }
            
                    case 405: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Request method not allowed! [GET, POST...]',
                            position: 'bottom-center',
                        });
            
                        break;
                    }
            
                    case 500: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Server confusing to handle!',
                            position: 'bottom-center',
                        });
            
                        break;
                    }
            
                    default: {
                        $.message({
                            type: 'error',
                            text: theErrorMessage ?? 'Unhanled error! Please check the DevTools Console.',
                            position: 'bottom-center',
                        });
                    }
                }
            
                return Promise.reject(err);
            });
    }
}
