#!/usr/bin/env python3

import yaml
import click
import os




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


def gen_dict_from_package_list(packages_list):
    packages_dict = dict()

    if packages_list == None:
        return packages_dict

    with open(packages_list) as file:
        Lines = file.readlines()
        for line in Lines:
            if line.startswith("Package: "):
                cur_package_name = line.split("Package: ", 2)[1].strip()
                packages_dict[cur_package_name] = dict()
                packages_dict[cur_package_name]["required-by-feature"] = "None"
            else:
                key = line.split(": ", 2)[0].strip()
                value = line.split(": ", 2)[1].strip()
                packages_dict[cur_package_name][key] = value
    return packages_dict


@click.command()
@click.option('--packages-mirror-all', type=click.Path(exists=True), help='Pre-formated list of debian packages (architecture independent)')
@click.option('--packages-mirror-amd64', type=click.Path(exists=True), help='Pre-formated list of debian packages available for amd64')
@click.option('--packages-mirror-arm64', type=click.Path(exists=True), help='Pre-formated list of debian packages available for arm64')
@click.option('--packages-gl-all', type=click.Path(exists=True), help='Pre-formated list of gardenlinux packages (architecture independent)')
@click.option('--packages-gl-amd64', type=click.Path(exists=True), help='Pre-formated list of gardenlinux packages available for amd64')
@click.option('--packages-gl-arm64', type=click.Path(exists=True), help='Pre-formated list of gardenlinix packages available for arm64')
@click.option('--feature-folder', type=click.Path(exists=True), help='gardenlinux/feature folder containing subfolders with pkg.include files')
@click.option('--output', type=click.Path(exists=False), help='Path to file where package.yaml will be written to')
@click.option('--required-only', is_flag=True,  default=False, help='If flag is set, only packages that are required by a feature will be included on output yaml')
def generate(packages_mirror_all, packages_mirror_amd64, packages_mirror_arm64, packages_gl_all, packages_gl_amd64, packages_gl_arm64, feature_folder, output, required_only):

    packages_mirror_all_dict = gen_dict_from_package_list(packages_mirror_all)
    packages_gl_all_dict = gen_dict_from_package_list(packages_gl_all)

    packages_mirror_amd64_dict = gen_dict_from_package_list(packages_mirror_amd64)
    packages_gl_amd64_dict = gen_dict_from_package_list(packages_gl_amd64)
    packages_mirror_arm64_dict = gen_dict_from_package_list(packages_mirror_arm64)
    packages_gl_arm64_dict = gen_dict_from_package_list(packages_gl_arm64)

    packages_gl_dict = dict()
    packages_mirror_dict = dict()
    packages_dict = dict()

    print("### dumping package dicts to yaml")
    packages_mirror_dict["all"] = packages_mirror_all_dict
    packages_mirror_dict["amd64"] = packages_mirror_amd64_dict
    packages_mirror_dict["arm64"] = packages_mirror_arm64_dict

    packages_gl_dict["all"] = packages_gl_all_dict
    packages_gl_dict["amd64"] = packages_gl_amd64_dict
    packages_gl_dict["arm64"] = packages_gl_arm64_dict

    packages_dict["gardenlinux"] = packages_gl_dict
    packages_dict["debian"] = packages_mirror_dict


    print("### reading features")
    pkg_include_dict = get_pkg_include_paths_dict(feature_folder)
    feature_pkg_dict = get_feature_pkg_dict(pkg_include_dict)

    print("### cross referencing available packages to feature pkg.include")

    for feature in feature_pkg_dict:
        print(f"cross referencing packages from feature: {feature}")
        for pkg in feature_pkg_dict[feature]:
            # print(f"fearure: {feature} has package: {pkg}")
            for dist in packages_dict:
                for arch in packages_dict[dist]:
                    pkg = pkg.replace("${arch}", arch)
                    if pkg in packages_dict[dist][arch]:
                        print(f"{pkg} in debian arm64")
                        packages_dict[dist][arch][pkg]["required-by-feature"] = feature

    if required_only:
        for dist in packages_dict:
            for arch in packages_dict[dist]:
                for pkg in list(packages_dict[dist][arch]):
                   if packages_dict[dist][arch][pkg]["required-by-feature"] == "None":
                       del packages_dict[dist][arch][pkg]


    print("### Debug: output files")
    with open("../feature_packages.yaml", 'w') as outfile:
        yaml.dump(feature_pkg_dict, outfile)

    with open(output, 'w') as outfile:
        yaml.dump(packages_dict, outfile)


if __name__ == '__main__':
    generate()




