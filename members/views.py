"""ویوهای عمومی و داشبورد برای اعضای صنف (Member)."""
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import SectionAccessRequiredMixin, AjaxFormMixin, AjaxDeleteMixin
from specializations.models import Specialization

from .forms import MemberForm
from .models import Member


# ---------------------------------------------------------------
# صفحات عمومی
# ---------------------------------------------------------------

class MemberListView(ListView):
    """صفحه‌ی «همه‌ی اعضا»: فهرست کامل اعضای صنف به همراه زمینه‌ی فعالیت هرکدام و امکان فیلتر."""
    model = Member
    template_name = "members/members.html"
    context_object_name = "members"
    paginate_by = 12

    def get_queryset(self):
        qs = Member.objects.filter(status=Member.STATUS_ACTIVE).prefetch_related("specializations")
        q = self.request.GET.get("q", "").strip()
        spec = self.request.GET.get("spec", "").strip()
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(city__icontains=q) | Q(membership_no__icontains=q))
        if spec:
            qs = qs.filter(specializations__slug=spec)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["specializations"] = Specialization.objects.all()
        ctx["current_q"] = self.request.GET.get("q", "")
        ctx["current_spec"] = self.request.GET.get("spec", "")
        return ctx


class FeaturedMemberListView(ListView):
    """صفحه‌ی «اعضای اصلی»: فقط اعضایی که برای نمایش ویژه علامت‌گذاری شده‌اند (is_featured)."""
    model = Member
    template_name = "members/featured_members.html"
    context_object_name = "members"

    def get_queryset(self):
        return (
            Member.objects.filter(status=Member.STATUS_ACTIVE, is_featured=True)
            .prefetch_related("specializations")
        )


class MemberDetailView(DetailView):
    """پروفایل هر عضو؛ زمینه‌های فعالیت و نمونه‌کارهای همان عضو نمایش داده می‌شود."""
    model = Member
    template_name = "members/member_detail.html"
    context_object_name = "member"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["works"] = self.object.completed_works.all()
        return ctx


# ---------------------------------------------------------------
# داشبورد (CRUD)
# ---------------------------------------------------------------

class MemberDashListView(SectionAccessRequiredMixin, ListView):
    required_section = "members"
    required_action = "view"
    model = Member
    template_name = "members/dashboard/member_list.html"
    context_object_name = "members"
    paginate_by = 20
    extra_context = {"active": "members"}


class MemberCreateView(SectionAccessRequiredMixin, AjaxFormMixin, CreateView):
    required_section = "members"
    required_action = "add"
    model = Member
    form_class = MemberForm
    fragment_template_name = "members/dashboard/fragments/_member_fields.html"
    modal_title = "افزودن عضو جدید"
    success_url = reverse_lazy("members:dash_member_list")


class MemberUpdateView(SectionAccessRequiredMixin, AjaxFormMixin, UpdateView):
    required_section = "members"
    required_action = "edit"
    model = Member
    form_class = MemberForm
    fragment_template_name = "members/dashboard/fragments/_member_fields.html"
    modal_title = "ویرایش عضو"
    success_url = reverse_lazy("members:dash_member_list")


class MemberDeleteView(SectionAccessRequiredMixin, AjaxDeleteMixin, DeleteView):
    required_section = "members"
    required_action = "delete"
    model = Member
    template_name = "core/dashboard/confirm_delete.html"
    success_url = reverse_lazy("members:dash_member_list")
