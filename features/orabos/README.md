## Feature: orabos
### Description
<website-feature>
This platform feature creates an artifact for ORA Baremetal OS. Which is exposing a KVM hypervisor via kubernetes.
</website-feature>

### Features
This feature creates a baremetal compatible image artifact as a `.qcow2` file.

### Unit testing

### Meta
|||
|---|---|
|type|platform|
|artifact|`.raw`,`.qcow2`|
|included_features|`kvm`,`khost`|
|excluded_features|None|
