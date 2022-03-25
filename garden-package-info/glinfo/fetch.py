#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re
import glinfo.common as glinfo

def get_debian_sectrack_info(package):
    pass



def get_feature_pkg_dict(pkg_include_dict):

    feature_pkg_dict = dict()
    for feature in pkg_include_dict:
        fpath = pkg_include_dict[feature]
        feature_pkg_dict.setdefault(feature, [])
        with open(fpath, 'r') as fp:
            for line in fp:
                if line.startswith('#') or line.isspace():
                    continue
                feature_pkg_dict[feature].append(line.strip())
    return feature_pkg_dict

def get_pkg_include_paths_dict(feature_root):

    pkg_include_dict = dict()
    for feature_dir in os.listdir(feature_root):
        cur_pkg_include_candidate = os.path.join(feature_root, feature_dir, "pkg.include")
        if os.path.isfile(cur_pkg_include_candidate):
            pkg_include_dict[feature_dir] = cur_pkg_include_candidate
    return pkg_include_dict


def gen_dict_from_package_list(packages_list, arch, keyfilter):
    packages_dict = dict()

    if packages_list == None:
        return packages_dict
    for line in packages_list.splitlines():
        if line.startswith("Package: "):
            cur_package_name = line.split("Package: ", 2)[1].strip()
            cur_package_name = cur_package_name.replace("${arch}", arch)
            packages_dict[cur_package_name] = dict()
            packages_dict[cur_package_name]["required-by-feature"] = "None"
        else:
            split = line.split(": ", 2)
            if len(split) < 2:
                continue
            key = split[0].strip()
            if key in keyfilter:
                continue
            value = split[1].strip()
            if "Version" in key:
                if re.search("garden", value, re.IGNORECASE):
                    packages_dict[cur_package_name]["Gardenlinux-Package"] = "yes"
                else:
                    packages_dict[cur_package_name]["Gardenlinux-Package"] = "no"

            packages_dict[cur_package_name][key] = value
    return packages_dict



def download_repo_pkg_file(arch, version):
    url = f"http://repo.gardenlinux.io/gardenlinux/dists/{version}/main/binary-{arch}/Packages"
    return glinfo.download_file(url)


@click.command()
@click.option('--feature-folder', default="../features", type=click.Path(exists=True), help='gardenlinux/feature folder containing subfolders with pkg.include files')
@click.option('--output', default="packages.yaml", type=click.Path(exists=False), help='Path to file where package.yaml will be written to')
@click.option('--required-only', is_flag=True,  default=False, help='If flag is set, only packages that are required by a feature will be included on output yaml')
def fetch(feature_folder, output, required_only):


    keyfilter = ['MD5sum', 'SHA1', 'SHA256', 'SHA512', 'Description-Md5',
                 'Breaks', 'Depends', 'Homepage', 'Maintainer', 'Tag', 'Built-Using', 'Build-Ids']

    packages_all_dict = gen_dict_from_package_list(download_repo_pkg_file("all", "dev"), "all", keyfilter)
    packages_amd64_dict = gen_dict_from_package_list(download_repo_pkg_file("amd64", "dev"), "amd64", keyfilter)
    packages_arm64_dict = gen_dict_from_package_list(download_repo_pkg_file("arm64", "dev"), "arm64", keyfilter)

    packages_dict = dict()

    print("### dumping package dicts to yaml")

    packages_dict["all"] = packages_all_dict
    packages_dict["amd64"] = packages_amd64_dict
    packages_dict["arm64"] = packages_arm64_dict

    print("### reading features")
    pkg_include_dict = get_pkg_include_paths_dict(feature_folder)
    feature_pkg_dict = get_feature_pkg_dict(pkg_include_dict)

    print("### cross referencing available packages to feature pkg.include")

    for feature in feature_pkg_dict:
        print(f"cross referencing packages from feature: {feature}")
        for pkg in feature_pkg_dict[feature]:
            # print(f"feature: {feature} has package: {pkg}")
                for arch in packages_dict:
                    arch_pkg = pkg.replace('${arch}',arch)
                    print(arch_pkg)
                    if arch_pkg in packages_dict[arch]:
                        packages_dict[arch][arch_pkg]["required-by-feature"] = feature

    if required_only:
            for arch in packages_dict:
                for pkg in list(packages_dict[arch]):
                   if packages_dict[arch][pkg]["required-by-feature"] == "None":
                       del packages_dict[arch][pkg]

    print("### Debug: output files")
    with open("../feature_packages.yaml", 'w') as outfile:
        yaml.dump(feature_pkg_dict, outfile)

    with open(output, 'w') as outfile:
        yaml.dump(packages_dict, outfile)

