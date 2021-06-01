# INSTALLATION CUDD IN MACOS #
## General ##
When we try to install the `dd.cudd` module in macOS laptops, we had some errors.
That probably caused due to an `SSL: CERTIFICATE_VERIFY_FAILED` error while the installation process tried to download the cudd package at first.
We manually downloaded the package and edited one of the `dd` files before the installation to avoid this error.

## Instructions ##
1. `sudo python3 -m pip download dd --no-deps`
2. `tar xzf dd-*.tar.gz`
3. `cd dd-*`
4. From https://sourceforge.net/projects/cudd-mirror/ download the cudd package.
5. Move the file (`cudd-3.0.0.tar.gz`) to the `dd-*` folder.
6. In the `dd-*` folder edit `download.py`:
   1. Replace the line: `fname = fetch(CUDD_URL, CUDD_SHA256)`
	with this line: `fname = "cudd-3.0.0.tar.gz"`
      (It is nearly at the end of the file).
6. `python3 setup.py install`

