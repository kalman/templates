#!/usr/bin/python
# Copyright 2013 Benjamin Kalman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from handlebar import Handlebar
import json
import os
import sys
import unittest

def _Read(name):
  test_data = os.path.join(
      sys.path[0], os.pardir, 'test', 'org', 'lman', 'template', 'data')
  with open(os.path.join(test_data, name), 'r') as f:
    return f.read()

class HandlebarTest(unittest.TestCase):
  def testCleanPartials(self):
    self._Run('cleanPartials', partials=('p1', 'p2'))
  def testCleanRendering(self):
    self._Run('cleanRendering', expect_errors=True)
  def testComment(self):
    self._Run('comment')
  def testDeepNulls(self):
    self._Run('deepNulls')
  def testDeepPartials(self):
    self._Run('deepPartials', partials=('partial',))
  def testElseRendering(self):
    self._Run('elseRendering')
  def testEmptyLists(self):
    self._Run('emptyLists')
  def testEmptySections(self):
    self._Run('emptySections')
  def testEscaping(self):
    self._Run('escaping')
  def testExistence(self):
    self._Run('existence')
  def testFlat(self):
    self._Run('flat')
  def testHasPartial(self):
    self._Run('hasPartial', partials=('partial',))
  def testIdentity(self):
    self._Run('identity')
  def testInvertedSections(self):
    self._Run('invertedSections', instance='0')
    self._Run('invertedSections', instance='1')
    self._Run('invertedSections', instance='2', expect_errors=True)
    self._Run('invertedSections', instance='3')
  def testJson(self):
    self._Run('json')
  def testMulti(self):
    self._Run('multi')
  def testNonexistence(self):
    self._Run('nonexistence')
  def testNonexistentName(self):
    self._Run('nonexistentName', expect_errors=True)
  def testNullsWithQuestion(self):
    self._Run('nullsWithQuestion')
  def testNullsWithSection(self):
    self._Run('nullsWithSection', expect_errors=True)
  def testObjectSections(self):
    self._Run('objectSections')
  def testOptionalEndSectionName(self):
    self._Run('optionalEndSectionName')
  def testPartialInheritance(self):
    self._Run('partialInheritance', partials=('p1',), expect_errors=True)
  def testPaths(self):
    self._Run('paths')
  def testSelfClosing(self):
    self._Run('selfClosing', partials=('p1',))
  def testStringPartialParams(self):
    self._Run('stringPartialParams', partials=('p1', 'p2'))
  def testThis(self):
    self._Run('this')
  def testValidIds(self):
    self._Run('validIds')

  def _Run(self, name, instance=None, partials=None, expect_errors=False):
    template = _Read('%s.template' % name)
    if instance is None:
      expected = _Read('%s.expected' % name)
      data = json.loads(_Read('%s.json' % name))
    else:
      expected = _Read('%s_%s.expected' % (name, instance))
      data = json.loads(_Read('%s_%s.json' % (name, instance)))
    if partials is not None:
      partial_data = {}
      for partial in partials:
        partial_name = '%s_%s' % (name, partial)
        partial_data[partial_name] = Handlebar(
            _Read('%s.template' % partial_name))
      data['partials'] = partial_data
    result = Handlebar(template).Render(data)
    if not expect_errors and result.errors:
      self.fail(''.join(result.errors))
    if expected != result.text:
      message = '\n'.join(('Expected:', expected.replace('\n', '$\n'),
                           'Got:', result.text.replace('\n', '$\n')))
      self.fail(message)

if __name__ == '__main__':
  unittest.main()
