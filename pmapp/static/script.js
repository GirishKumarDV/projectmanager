function logout() {
    var login_url = '../templates/login.html';
    window.open(login_url, '_blank')
    this.close()
}