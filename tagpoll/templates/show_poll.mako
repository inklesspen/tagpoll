<%! import random %>
<%inherit file="tagpoll:templates/base.mako"/>
<script type="text/ng-template" id="tagbutton.html">
<span>
<button type="button" class="btn btn-lg" ng-class="{'btn-default': !selected, 'btn-info': selected}" ng-disabled="collection.length >= max &amp;&amp; !selected ">{{tag}}</button>
<input type="checkbox" name="tag" value="{{tag}}" class="tag-checkbox" ng-model="selected">
</span>
</script>
<div ng-controller="PollController">
<form action="${request.route_path('vote')}" method="post" accept-charset="utf-8">
  

<p class="lead">${text}</p>
<p>Select ${ max if max == min else "between {} and {}".format(min, max) } options to vote, or choose to skip voting and just see the results.</p>
<div id="tagbuttons" data-min=${min} data-max=${max} class="form-group">
<%
tag_list = list(tags)
random.shuffle(tag_list) 
%>
% for tag in tag_list:
<div tag-button="${tag}" collection="tags"></div>
% endfor
</div>
  <div class="form-group">
  
<button type="submit" class="btn btn-primary btn-lg" ng-disabled="tags.length < min || tags.length > max">Vote and See Results</button>
</div>
</form>
<form action="${request.route_path('vote')}" method="post" accept-charset="utf-8">
  <input type="hidden" name="skipped" value="skipped" id="skipped">
  <p>If you skip voting, you will not be able to come back and vote later; I want you to vote without being influenced by the results.</p>
    <p>
  <button type="submit" class="btn btn-danger btn-lg">Skip Voting and See Results</button>
  </p>
</form>
</div>