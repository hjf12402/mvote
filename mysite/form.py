from django.forms import ModelForm
from .models import Poll, PollItem

class AddPoll(ModelForm):
    class Meta:
        model = Poll
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddPoll, self).__init__(*args, **kwargs)
        self.fields['name'].label = '你要发起的项目主题'

class AddItem(ModelForm):
    class Meta:
        model = PollItem
        fields = ['name', 'image_url']

    def __init__(self, *args, **kwargs):
        super(AddItem, self).__init__(*args, **kwargs)
        self.fields['name'].label = '投票选项名称'
        self.fields['image_url'].label = '图片url'