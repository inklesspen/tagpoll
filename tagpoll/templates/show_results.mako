<%! import json %>
<%inherit file="tagpoll:templates/base.mako"/>
<p class="lead">The poll question was:<br>${question.text}</p>
<p>So far there have been ${votes} votes.</p>
<p>Top choices:<br>
  <table>
    <tbody>
% for tag in ordered_tags[:10]:
      <tr><td>${tag}</td><td>${tags[tag]}</td></tr>
% endfor
    </tbody>
  </table>
</p>
<p>All results:<br>
    <div id="chart_div" ></div>
    </p>

<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(drawChart);
  function drawChart() {
<% 
tag_count_list = [[tag, tags[tag]] for tag in question.tags]
tag_count_list.sort(key=lambda pair: pair[0])
tag_count_list.insert(0, ["Value", "Votes"])
%>
    var data = google.visualization.arrayToDataTable(${tag_count_list | n, json.dumps});

    var options = {
      'hAxis': {
        'format': '####',
        'ticks': ${list(range(votes+1)) | n, json.dumps}
      },
      'legend': {
        'position': 'none'
      },
      'chartArea': {
        'width': '80%',
        'height': '90%'
      }
    };

    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
</script>