##############
sequential tar
##############
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|

A wrapper around ``tarfile`` which is deliberatly limited and simple.
This ``sequential_tar`` can not seek. Files are read and written file by file.
This package is only meant to read and write tar files with less code clutter
for the special case of sequential adding or extraction of files.
While writing/reding, for each file one can specify a mode
such as [``b``,``t``] for either binary or text mode and
optinally ``|gz`` for compression.


.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/sequential_tar/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/sequential_tar/actions/workflows/test.yml

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/sequential_tar
    :target: https://pypi.org/project/sequential_tar

.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |BlackPackStyle| image:: https://img.shields.io/badge/pack%20style-black-000000.svg
    :target: https://github.com/cherenkov-plenoscope/black_pack

.. |MITLicenseBadge| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

