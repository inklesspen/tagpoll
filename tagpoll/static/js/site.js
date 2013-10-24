//
angular.module('tagpoll', []).
  directive('tagButton', function() {
    return {
      restrict: 'A',
      scope: {tag: '@tagButton', collection: '='},
      templateUrl: 'tagbutton.html',
      replace: true,
      link: function(scope, elm, attrs) {
        scope.max = $("#tagbuttons").data('max');

        scope.selected = false;
        elm.bind('click', function() {
          scope.$apply(function() {
            scope.selected = !scope.selected;
          });
        });
        scope.$watch('selected', function selected_watcher(val) {
          if (val) {
            scope.collection.push(scope.tag);
          } else {
            _.remove(scope.collection, function(item) {
              return item === scope.tag;
            });
          }
        });
      }
    };
  }).
  controller('PollController', function PollController($scope) {
    $scope.tags = [];
    $scope.max = $("#tagbuttons").data('max');
    $scope.min = $("#tagbuttons").data('min');
  });
