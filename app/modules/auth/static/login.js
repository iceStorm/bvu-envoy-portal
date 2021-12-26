/* eslint-disable */
function loginForm() {
  return {
    _email: '',

    init() {
      this.$watch('_email', (value) => {
        this.checkEmailExist(value);
      });
    },
    checkEmailExist(value) {
      console.log(document.getElementById('email').validity);

      if (!document.getElementById('email').validity.typeMismatch) {
        const checkEmailFormData = new FormData();
        checkEmailFormData.append('email', value);

        axios.post('/check-email', checkEmailFormData)
          .then((res) => {
            console.log(res);
            document.getElementById('email').setCustomValidity('');
          })
          .catch((err) => {
            console.log(err);
            document.getElementById('email').setCustomValidity('The email is not registered');
          });
      }
    },
  };
}
