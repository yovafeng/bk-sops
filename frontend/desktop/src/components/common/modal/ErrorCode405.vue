/**
* Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
* Edition) available.
* Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
* Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://opensource.org/licenses/MIT
* Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
* an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
* specific language governing permissions and limitations under the License.
*/
<template>
    <div class="content-wrapper">
        <h3 class="error-title">{{ $t('对不起，您没有当前操作需要的的权限') }}</h3>
        <ul>
            <li>{{ $t('1.联系项目运维为您添加') }}
                <a href="javascript:void(0);" @click.prevent="onGotoCC">{{ $t('配置平台') }}</a>
                {{ $t('对应项目的角色，如运维人员、开发人员、产品人员、测试人员') }}
            </li>
            <li>{{ $t('2.联系项目运维为您添加需要操作的流程模板的权限') }}</li>
            <li>{{ $t('3.或者前往') }}
                <a href="javascript:void(0);" @click.prevent="onGotoCC">{{ $t('配置平台') }}</a>
                {{ $t('创建属于自己的项目') }}
            </li>
        </ul>
        <p v-if="responseText" class="error-tip">{{responseText}}</p>
    </div>
</template>
<script>
    import openOtherApp from '@/utils/openOtherApp.js'

    export default {
        name: 'ErrorCode405',
        props: ['responseText'],
        methods: {
            onGotoCC () {
                openOtherApp('bk_cmdb', window.BK_CC_HOST)
            }
        }
    }
</script>
<style lang="scss" scoped>
@import '@/scss/config.scss';
ul {
    padding-left: 30px;
}
li {
    list-style: disc;
}
.error-tip {
    margin-top: 10px;
    color: $redDark;
    text-align: left;
}
</style>
