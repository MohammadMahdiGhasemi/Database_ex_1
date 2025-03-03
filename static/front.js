// گرفتن المان‌های مورد نیاز
const modal = document.getElementById("my-modal");
const modalBtn = document.getElementById("modal-btn");
const closeBtn = document.querySelector(".close");
const form = document.getElementById("insert-form");
const deleteButtons = document.querySelectorAll(".delete-btn");

// نمایش مودال
modalBtn.onclick = function() {
    modal.style.display = "block";
}

// بستن مودال
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// بستن مودال با کلیک خارج از آن
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// مدیریت فرم
form.onsubmit = function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    fetch('/insert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            modal.style.display = "none";
            form.reset();
            window.location.reload();
        } else {
            alert('خطا در ثبت اطلاعات');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('خطا در ارتباط با سرور');
    });
}

// تأییدیه حذف
deleteButtons.forEach(button => {
    button.onclick = function(e) {
        e.preventDefault();
        if (confirm('آیا از حذف این رکورد اطمینان دارید؟')) {
            window.location.href = this.href;
        }
    }
}); 