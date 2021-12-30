var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __markAsModule = (target) => __defProp(target, "__esModule", { value: true });
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[Object.keys(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __reExport = (target, module, desc) => {
  if (module && typeof module === "object" || typeof module === "function") {
    for (let key of __getOwnPropNames(module))
      if (!__hasOwnProp.call(target, key) && key !== "default")
        __defProp(target, key, { get: () => module[key], enumerable: !(desc = __getOwnPropDesc(module, key)) || desc.enumerable });
  }
  return target;
};
var __toModule = (module) => {
  return __reExport(__markAsModule(__defProp(module != null ? __create(__getProtoOf(module)) : {}, "default", module && module.__esModule && "default" in module ? { get: () => module.default, enumerable: true } : { value: module, enumerable: true })), module);
};

// src/js/src.js
var require_app = __commonJS({
  "src/js/src.js"(exports, module) {
    "use strict";
    module.exports = class App {
      constructor({
        backendEndpoint = "/",
        scrollTopButton = {
          visible: true,
          offset: 200
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
        loadProgressBar({
          speed: 450,
          trickleRate: 0.02,
          trickleSpeed: 1750,
          showSpinner: false
        });
      }
      initTippy() {
        tippy("[data-tippy-content]");
      }
      initAxios() {
        axios.defaults.baseURL = this.backendEndpoint;
        axios.defaults.withCredentials = true;
        this.setAxiosResponseInterceptor();
      }
      setupScrollTopButton() {
        console.log(this.scrollTopButton);
      }
      setAxiosResponseInterceptor() {
        axios.interceptors.response.use((res) => {
          return res;
        }, (err) => {
          console.log("axios error response:", err.response.status);
          const theErrorMessage = err.response?.data?.message;
          switch (err.response.status) {
            case 400: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Bad request! Please check your request data.",
                position: "bottom-center"
              });
              break;
            }
            case 401: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Not authenticated. Please login first!",
                position: "bottom-center"
              });
              break;
            }
            case 403: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Forbidden, please return!",
                position: "bottom-center"
              });
              break;
            }
            case 404: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Resource not found!",
                position: "bottom-center"
              });
              break;
            }
            case 405: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Request method not allowed! [GET, POST...]",
                position: "bottom-center"
              });
              break;
            }
            case 429: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Too many requests, please calm down..",
                position: "bottom-center"
              });
              break;
            }
            case 500: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Server confusing to handle!",
                position: "bottom-center"
              });
              break;
            }
            default: {
              $.message({
                type: "error",
                text: theErrorMessage ?? "Unhanled error! Please check the DevTools Console.",
                position: "bottom-center"
              });
            }
          }
          return Promise.reject(err);
        });
      }
    };
  }
});

// src/js/base.js
var import_app = __toModule(require_app());
var app = new import_app.default({
  backendEndpoint: "/",
  scrollTopButton: {
    visible: false
  }
});
function showToast(text, type, duration = 5e3) {
  $.message({
    type,
    text,
    duration,
    position: "bottom-center"
  });
}
setATagNavigate();
function setATagNavigate() {
  $("a:not(.not-ajax)").each(function(index, elem) {
    $(this).unbind("click").click((e) => {
      e.preventDefault();
      const href = $(this).attr("href");
      navigateTo(href);
    });
  });
}
$(window).on("popstate", function(e) {
  console.log("\back pressed:", location.href);
  navigateTo(location.href);
});
function navigateTo(path) {
  axios.get(path).then((res) => {
    replaceContent(res);
  }).catch((err) => {
    console.log(err);
  });
}
function replaceContent(axiosResponse) {
  const html = axiosResponse.data;
  const path = axiosResponse.request.responseURL;
  const ajaxContent = $("<div>").append($.parseHTML(html, document, true));
  $("#main").html(ajaxContent.find("#main").html());
  $("#nav").html(ajaxContent.find("#nav").html());
  window.history.pushState("", "", `${path}`);
  src.initTippy();
  setATagNavigate();
  setSubmit();
}
setSubmit();
function setSubmit() {
  $("form.ajax").each(function(index, elem) {
    $(this).submit((e) => {
      e.preventDefault();
      let query_params = {};
      if (e.target.method == "get") {
        $(e.target).find("input").each(function() {
          if (this.type != "submit")
            query_params[this.name] = this.value;
        });
      }
      axios.request({
        method: e.target.method,
        url: e.target.action,
        data: e.target.method == "post" ? new FormData(e.target) : null,
        params: query_params
      }).then((res) => {
        replaceContent(res);
      }).catch((err) => {
        showToast(err.response.data.message, "error");
        console.log(err);
      });
    });
  });
}
