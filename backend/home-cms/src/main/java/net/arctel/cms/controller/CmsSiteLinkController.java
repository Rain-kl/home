/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package net.arctel.cms.controller;

import cn.dev33.satoken.stp.StpUtil;
import jakarta.annotation.Resource;
import jakarta.validation.Valid;
import java.util.List;
import net.arctel.cms.entity.CmsSiteLink;
import net.arctel.cms.input.SiteLinkInput;
import net.arctel.cms.service.CmsSiteLinkService;
import net.arctel.platform.framework.utils.Result;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
public class CmsSiteLinkController {

    @Resource
    private CmsSiteLinkService cmsSiteLinkService;

    @GetMapping("/pub/site-links")
    public Result<List<CmsSiteLink>> listEnabled() {
        return Result.success(cmsSiteLinkService.listEnabled());
    }

    @GetMapping("/cms/site-links")
    public Result<List<CmsSiteLink>> listAll() {
        StpUtil.checkLogin();
        return Result.success(cmsSiteLinkService.listAll());
    }

    @PostMapping("/cms/site-links")
    public Result<Boolean> replaceAll(@RequestBody List<@Valid SiteLinkInput> inputList) {
        StpUtil.checkLogin();
        return Result.success(cmsSiteLinkService.replaceAll(inputList));
    }
}
