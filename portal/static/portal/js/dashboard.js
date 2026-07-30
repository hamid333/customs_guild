/* ==========================================================================
   داشبورد انجمن — Select2 + تقویم شمسی (persian-datepicker) + مودال‌های
   افزودن/ویرایش/حذف با SweetAlert2 (بدون بارگذاری مجدد صفحه برای هر فیلد)
   ========================================================================== */

/** مقداردهی اولیه‌ی Select2 روی تمام فیلدهای دارای کلاس select2-field داخل یک بازه (scope). */
function initSelect2(scope) {
  if (typeof $ === "undefined" || !$.fn.select2) return;
  $(scope).find(".select2-field").each(function () {
    $(this).select2({
      dir: "rtl",
      width: "100%",
      dropdownParent: $(this).closest(".swal2-html-container").length ? $(this).closest(".swal2-html-container") : $(document.body),
      language: {
        noResults: function () { return "موردی یافت نشد"; },
        searching: function () { return "در حال جست‌وجو..."; },
      },
    });
  });
}

/** مقداردهی اولیه‌ی تقویم شمسی روی فیلدهای تاریخ (jalali-datepicker) و تاریخ‌وساعت (jalali-datetimepicker). */
function initJalaliDatepickers(scope) {
  if (typeof $ === "undefined" || !$.fn.persianDatepicker) return;
  $(scope).find(".jalali-datepicker").each(function () {
    $(this).persianDatepicker({
      format: "YYYY/MM/DD",
      autoClose: true,
      initialValue: false,
      observer: true,
    });
  });
  $(scope).find(".jalali-datetimepicker").each(function () {
    $(this).persianDatepicker({
      format: "YYYY/MM/DD HH:mm",
      timePicker: { enabled: true },
      autoClose: true,
      initialValue: false,
      observer: true,
    });
  });
}

/** خواندن مقدار یک کوکی (برای گرفتن توکن CSRF جنگو جهت درخواست حذف). */
function getCookie(name) {
  const match = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
  return match ? decodeURIComponent(match.pop()) : "";
}

/** باز کردن مودال افزودن/ویرایش: فرم را به‌صورت AJAX از سرور می‌گیرد و داخل SweetAlert2 نمایش می‌دهد. */
function openFormModal(url, title) {
  fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
    .then(function (res) { return res.text(); })
    .then(function (html) {
      Swal.fire({
        title: title,
        html: html,
        width: 640,
        showCancelButton: true,
        confirmButtonText: "ذخیره",
        cancelButtonText: "انصراف",
        focusConfirm: false,
        didOpen: function () {
          const container = Swal.getHtmlContainer();
          initSelect2(container);
          initJalaliDatepickers(container);
        },
        preConfirm: function () {
          const form = document.getElementById("modalForm");
          const formData = new FormData(form);
          return fetch(url, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: formData,
          })
            .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
            .then(function (result) {
              if (!result.data.success) {
                const container = Swal.getHtmlContainer();
                container.innerHTML = result.data.html;
                initSelect2(container);
                initJalaliDatepickers(container);
                Swal.showValidationMessage("لطفاً خطاهای فرم را بررسی کنید.");
                return false;
              }
              return true;
            })
            .catch(function () {
              Swal.showValidationMessage("خطا در برقراری ارتباط با سرور. دوباره تلاش کنید.");
              return false;
            });
        },
        allowOutsideClick: function () { return !Swal.isLoading(); },
      }).then(function (result) {
        if (result.isConfirmed) {
          Swal.fire({ icon: "success", title: "با موفقیت ذخیره شد", timer: 1300, showConfirmButton: false })
            .then(function () { window.location.reload(); });
        }
      });
    })
    .catch(function () {
      Swal.fire({ icon: "error", title: "خطا", text: "بارگذاری فرم با مشکل مواجه شد." });
    });
}

/** نمایش مودال تأیید حذف و ارسال درخواست حذف در صورت تأیید کاربر. */
function confirmDeleteModal(url, name) {
  Swal.fire({
    title: "حذف شود؟",
    text: name ? "آیا از حذف «" + name + "» مطمئن هستید؟ این عملیات قابل بازگشت نیست." : "آیا از حذف این مورد مطمئن هستید؟",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "بله، حذف شود",
    cancelButtonText: "انصراف",
    confirmButtonColor: "#c0392b",
  }).then(function (result) {
    if (!result.isConfirmed) return;
    fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.success) {
          Swal.fire({ icon: "success", title: "حذف شد", timer: 1100, showConfirmButton: false })
            .then(function () { window.location.reload(); });
        } else {
          Swal.fire({ icon: "error", title: "خطا", text: "حذف با مشکل مواجه شد." });
        }
      })
      .catch(function () {
        Swal.fire({ icon: "error", title: "خطا", text: "برقراری ارتباط با سرور با مشکل مواجه شد." });
      });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  initSelect2(document);
  initJalaliDatepickers(document);

  document.body.addEventListener("click", function (e) {
    const formBtn = e.target.closest("[data-modal-form]");
    if (formBtn) {
      e.preventDefault();
      openFormModal(formBtn.getAttribute("data-url"), formBtn.getAttribute("data-title") || "");
      return;
    }
    const delBtn = e.target.closest("[data-modal-delete]");
    if (delBtn) {
      e.preventDefault();
      confirmDeleteModal(delBtn.getAttribute("data-url"), delBtn.getAttribute("data-name") || "");
    }
  });
});
