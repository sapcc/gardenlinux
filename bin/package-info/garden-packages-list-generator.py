#!/usr/bin/env python3

import yaml
import click



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
@click.option('--output', type=click.Path(exists=False), help='Path to file where package.yaml will be written to')
def generate(packages_mirror_all, packages_mirror_amd64, packages_mirror_arm64, packages_gl_all, packages_gl_amd64, packages_gl_arm64, output):

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

    with open(output, 'w') as outfile:
        yaml.dump(packages_dict, outfile)


if __name__ == '__main__':
    generate()




