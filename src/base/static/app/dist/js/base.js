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
var __reExport = (target, module2, desc) => {
  if (module2 && typeof module2 === "object" || typeof module2 === "function") {
    for (let key of __getOwnPropNames(module2))
      if (!__hasOwnProp.call(target, key) && key !== "default")
        __defProp(target, key, { get: () => module2[key], enumerable: !(desc = __getOwnPropDesc(module2, key)) || desc.enumerable });
  }
  return target;
};
var __toModule = (module2) => {
  return __reExport(__markAsModule(__defProp(module2 != null ? __create(__getProtoOf(module2)) : {}, "default", module2 && module2.__esModule && "default" in module2 ? { get: () => module2.default, enumerable: true } : { value: module2, enumerable: true })), module2);
};

// src/js/app.js
var require_app = __commonJS({
  "src/js/app.js"(exports2, module2) {
    "use strict";
    module2.exports = class App {
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
        AOS.init();
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
        tippy("[data-tippy-content]", {
          interactive: true,
          allowHTML: true,
          theme: "light"
        });
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
function setATagNavigate() {
  $(".ajax)").each(function(index, elem) {
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
    showToast(err, "error");
  });
}
function replaceContent(axiosResponse) {
  const html = axiosResponse.data;
  const path = axiosResponse.request.responseURL;
  console.log("to:" + path);
  const ajaxContent = $("<div>").append($.parseHTML(html, document, true));
  $("html").html(ajaxContent);
  window.history.pushState("", "", `${path}`);
  app.initTippy();
  setATagNavigate();
  setSubmit();
}
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
