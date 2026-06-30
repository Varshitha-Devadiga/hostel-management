document.addEventListener('DOMContentLoaded', function() {
  const avatarInput = document.querySelector('.ag-hidden-file-input[type="file"]');
  const avatarImg = document.querySelector('.ag-profile-main-avatar');
  const avatarPlaceholder = document.querySelector('.ag-profile-main-avatar-placeholder');

  if (avatarInput) {
    avatarInput.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        if (avatarImg) {
          avatarImg.src = e.target.result;
        } else if (avatarPlaceholder) {
          // Replace placeholder with img element
          const img = document.createElement('img');
          img.src = e.target.result;
          img.alt = 'Profile Photo';
          img.className = 'ag-profile-main-avatar';
          avatarPlaceholder.replaceWith(img);
        }
      };
      reader.readAsDataURL(file);
    });
  }
});
