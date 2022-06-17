from pipes import Template
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from crud.forms import ProcessForm, ProtocolForm
from .models import Protocol, Process
from django.db import transaction


@login_required
def create_protocol(request):
    template_name= "create.html"
    # min_num, validate_min=Trueによって、必ず入力される
    ProtocolFormset= modelformset_factory(model=Protocol, form=ProtocolForm,
                                          max_num=1, min_num=1,validate_min=True)
    
    if request.method == "GET":
        formset_protocol= ProtocolFormset(None,queryset=Protocol.objects.none())
        context = {
            'formset_protocol': formset_protocol,
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        formset_protocol= ProtocolFormset(request.POST,queryset=Protocol.objects.none())
        if formset_protocol.is_valid():
            protocol_ob= formset_protocol.save(commit=False)
            for ob in protocol_ob:  # formset.save(commit=False)はリストを返すことに注意
                ob.user= request.user
                ob.save()
            return redirect(reverse("crud:create2",args=[ob.pk]))
        else:  # is_valid false
            # formset_protocol= ProtocolFormset(queryset=Protocol.objects.none())
            context = {
                'formset_protocol': formset_protocol,
                'error_message' : "不備があります",
            }
            return render(request, template_name, context)


@login_required
def create_process(request,pk):
    template_name= "create2.html"
    # inlineformset
    ProcessFormset= inlineformset_factory(parent_model=Protocol,model=Process, form=ProcessForm, 
                                         max_num=1, min_num=1, validate_min=True)
    parent= Protocol.objects.get(pk=pk)

    if request.method == "GET":
        # Protocol object 作成者とログインユーザーの一致を確認
        if not parent.user == request.user:
            return redirect("crud:home")

        formset_process= ProcessFormset(None, instance=parent, queryset=Process.objects.none())
        context = {
            'formset_process': formset_process,
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data= request.POST  # post dataの取得
        title_list = post_data.getlist("process_set-0-title")
        content_list = post_data.getlist("process_set-0-content")
        time_0_list = post_data.getlist("process_set-0-time_0")
        time_1_list = post_data.getlist("process_set-0-time_1")
        time_2_list = post_data.getlist("process_set-0-time_2")
        sub_list = post_data.getlist("process_set-0-sub")
        rank_list = post_data.getlist("process_set-0-rank")
        total_num= post_data.get("process_set-TOTAL_FORMS")
        #
        insert_data = {
            'process_set-TOTAL_FORMS': total_num,
            'process_set-INITIAL_FORMS': '0',
            'process_set-MAX_NUM_FORMS': '',
        }
        for i in range(int(total_num)):
            insert_data[f"process_set-{i}-title"] = title_list[i]
            insert_data[f"process_set-{i}-content"] = content_list[i]
            insert_data[f"process_set-{i}-time_0"] = time_0_list[i]
            insert_data[f"process_set-{i}-time_1"] = time_1_list[i]
            insert_data[f"process_set-{i}-time_2"] = time_2_list[i]
            insert_data[f"process_set-{i}-sub"] = sub_list[i]
            insert_data[f"process_set-{i}-rank"] = rank_list[i]
        # form set 作成
        formset_process= ProcessFormset(insert_data, instance=parent, queryset=Process.objects.none())
        if formset_process.is_valid():
            formset_process.save()
            # with transaction.atomic():
            #     for ob in process_ob:
            #         ob.protocol= Protocol.objects.get(pk=pk)
            #         ob.save()
            return redirect(reverse("crud:mypost"))
        else:  # is_valid false
            formset_process= ProcessFormset(queryset=Process.objects.none())
            context = {
                'formset_process': formset_process,
                'error_message' : "不備があります",
            }
            return render(request, template_name, context)
                

     

class Home(LoginRequiredMixin, ListView):
   """HOMEページで、自分以外のユーザー投稿をリスト表示"""
   model = Protocol
   template_name = 'list.html'

   def get_queryset(self):
       #リクエストユーザーのみ除外
       return Protocol.objects.exclude(user=self.request.user)
      
   
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Protocol
    template_name = 'list.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Protocol.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["place"]= "mypost"
        return context


class DetailPost(LoginRequiredMixin, DetailView):
    model= Protocol
    template_name= 'detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["process"]= Process.objects.filter(protocol=Protocol.objects.get(pk=pk)).order_by("-rank").reverse()
        return context

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   """投稿編集ページ"""
   model = Protocol
   template_name = 'update.html'
   fields = ['title', 'content']

   def get_success_url(self,  **kwargs):
       """編集完了後の遷移先"""
       pk = self.kwargs["pk"]
       return reverse_lazy('crud:detail', kwargs={"pk": pk})
   
   def test_func(self, **kwargs):
       """アクセスできるユーザーを制限"""
       pk = self.kwargs["pk"]
       post = Protocol.objects.get(pk=pk)
       return (post.user == self.request.user)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   """投稿編集ページ"""
   model = Protocol
   template_name = 'delete.html'
   success_url = reverse_lazy('crud:mypost')

   def test_func(self, **kwargs):
       """アクセスできるユーザーを制限"""
       pk = self.kwargs["pk"]
       post = Protocol.objects.get(pk=pk)
       return (post.user == self.request.user) 