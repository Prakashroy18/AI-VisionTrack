document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  firebase.auth().signInWithEmailAndPassword(email, password)
    .then(userCredential => {
      alert('Login successful!');
      // Redirect or update UI here
    })
    .catch(error => {
      alert(error.message);
    });
});

<script src="static/js/app.js"></script>