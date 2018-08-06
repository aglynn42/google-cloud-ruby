# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging
import re

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

# Temporary until we get Ruby-specific tools into synthtool
def merge_gemspec(src, dest, path):
    regex = re.compile(r'^\s+gem.version\s*=\s*"[\d\.]+"$', flags=re.MULTILINE)
    match = regex.search(dest)
    if match:
        src = regex.sub(match.group(0), src, count=1)
    regex = re.compile(r'^\s+gem.homepage\s*=\s*"[^"]+"$', flags=re.MULTILINE)
    match = regex.search(dest)
    if match:
        src = regex.sub(match.group(0), src, count=1)
    return src

v2_library = gapic.ruby_library(
    'dialogflow', 'v2',
    config_path='/google/cloud/dialogflow/artman_dialogflow_v2.yaml',
    artman_output_name='google-cloud-ruby/google-cloud-dialogflow'
)
s.copy(v2_library / 'lib')
s.copy(v2_library / 'test')
s.copy(v2_library / 'Rakefile')
s.copy(v2_library / 'README.md')
s.copy(v2_library / 'LICENSE')
s.copy(v2_library / '.gitignore')
s.copy(v2_library / '.rubocop.yml')
s.copy(v2_library / '.yardopts')
s.copy(v2_library / 'google-cloud-dialogflow.gemspec', merge=merge_gemspec)

# https://github.com/googleapis/gapic-generator/issues/2174
s.replace(
    'lib/google/cloud/dialogflow.rb',
    'File\.join\(dir, "\.rb"\)',
    'dir + ".rb"')

# https://github.com/googleapis/gapic-generator/issues/2182
s.replace(
    'lib/google/cloud/dialogflow/v2/credentials.rb',
    'DIALOGFLOW_KEYFILE\\n(\s+)DIALOGFLOW_CREDENTIALS\n',
    'DIALOGFLOW_CREDENTIALS\\n\\1DIALOGFLOW_KEYFILE\n')
s.replace(
    'lib/google/cloud/dialogflow/v2/credentials.rb',
    'DIALOGFLOW_KEYFILE_JSON\\n(\s+)DIALOGFLOW_CREDENTIALS_JSON\n',
    'DIALOGFLOW_CREDENTIALS_JSON\\n\\1DIALOGFLOW_KEYFILE_JSON\n')

# https://github.com/googleapis/gapic-generator/issues/2194
s.replace(
    '.yardopts',
    '\n--markup markdown\n\n',
    '\n--markup markdown\n--markup-provider redcarpet\n\n')

# https://github.com/googleapis/gapic-generator/issues/2194
s.replace(
    'google-cloud-dialogflow.gemspec',
    '\n  gem\\.add_development_dependency "minitest", "~> ([\\d\\.]+)"\n  gem\\.add_development_dependency "rubocop"',
    '\n  gem.add_development_dependency "minitest", "~> \\1"\n  gem.add_development_dependency "redcarpet", "~> 3.0"\n  gem.add_development_dependency "rubocop"')
s.replace(
    'google-cloud-dialogflow.gemspec',
    '\n  gem\\.add_development_dependency "simplecov", "~> ([\\d\\.]+)"\nend',
    '\n  gem.add_development_dependency "simplecov", "~> \\1"\n  gem.add_development_dependency "yard", "~> 0.9"\nend')

# https://github.com/googleapis/gapic-generator/issues/2195
s.replace(
    [
      'README.md',
      'lib/google/cloud/dialogflow.rb',
      'lib/google/cloud/dialogflow/v2.rb',
      'lib/google/cloud/dialogflow/v2/doc/overview.rb'
    ],
    '\\(https://console\\.cloud\\.google\\.com/apis/api/dialogflow\\)',
    '(https://console.cloud.google.com/apis/library/dialogflow.googleapis.com)')
